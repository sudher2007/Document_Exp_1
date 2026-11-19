import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  FileText, Upload, Send, Trash2, RefreshCw, Copy, Check,
  Settings as SettingsIcon, Download, ShieldCheck, Sparkles,
  BookOpen, ChevronDown, ChevronUp, List, Search,
  AlignLeft, Tags, FileSearch, FileInput, X, Plus, CheckCircle2
} from 'lucide-react';
import './App.css';

const API_BASE = 'http://localhost:8000/api';

// Quick action definitions
const DOC_ACTIONS = [
  { id: 'summarize', label: 'Summarize', icon: AlignLeft,  color: '#2563eb', bg: '#eff6ff', desc: 'Full document summary' },
  { id: 'keypoints', label: 'Key Points', icon: List,       color: '#7c3aed', bg: '#f5f3ff', desc: 'Most important points' },
  { id: 'outline',   label: 'Outline',    icon: FileSearch, color: '#059669', bg: '#ecfdf5', desc: 'Structure & sections' },
  { id: 'entities',  label: 'Entities',   icon: Tags,       color: '#d97706', bg: '#fffbeb', desc: 'People, dates & more' },
];

export default function App() {
  const [sessionId, setSessionId]     = useState('');
  const [document, setDocument]       = useState(null);
  const [messages, setMessages]       = useState([]);
  const [query, setQuery]             = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isAnswering, setIsAnswering] = useState(false);
  const [runningAction, setRunningAction] = useState(null); // 'summarize' | 'keypoints' | ...
  const [isDragging, setIsDragging]   = useState(false);
  const [copiedIndex, setCopiedIndex] = useState(null);
  const [expandedSources, setExpandedSources] = useState({});
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [confirmReplace, setConfirmReplace] = useState(false);
  const [pendingFile, setPendingFile] = useState(null);
  const [statusMsg, setStatusMsg]     = useState('');
  const [showPolicyCard, setShowPolicyCard] = useState(true);

  // Settings state
  const [apiKey, setApiKey]       = useState('');
  const [modelName, setModelName] = useState('gemini-2.5-flash');
  const [temperature, setTemperature] = useState(0.2);
  const [hasApiKey, setHasApiKey] = useState(false);
  const [sysPrompt, setSysPrompt] = useState('');

  const messagesEndRef = useRef(null);
  const fileInputRef   = useRef(null);

  // ─── Init ────────────────────────────────────────────────────────────────
  useEffect(() => {
    let sid = localStorage.getItem('doc_qa_sid');
    if (!sid) {
      sid = 'sess_' + Math.random().toString(36).slice(2, 11) + Date.now().toString(36);
      localStorage.setItem('doc_qa_sid', sid);
    }
    setSessionId(sid);

    fetch(`${API_BASE}/settings/`)
      .then(r => r.json())
      .then(d => {
        setHasApiKey(d.has_api_key);
        setModelName(d.model_name || 'gemini-2.5-flash');
        setTemperature(d.temperature || 0.2);
        setSysPrompt(d.system_prompt || '');
      }).catch(() => {});
  }, []);

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, isAnswering]);

  const flash = (msg) => { setStatusMsg(msg); setTimeout(() => setStatusMsg(''), 4000); };

  // ─── Load College Policy ─────────────────────────────────────────────────
  const loadPolicy = async (sid = sessionId) => {
    setIsUploading(true);
    flash('Loading Meridian College Policy Manual…');
    try {
      const r = await fetch(`${API_BASE}/load-policy-pdf/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sid })
      });
      const d = await r.json();
      if (r.ok) { setDocument(d.document); setMessages([]); flash('College Policy Manual ready!'); }
      else alert(d.error || 'Failed.');
    } catch { alert('Server error.'); }
    finally { setIsUploading(false); }
  };

  // ─── Upload any document ─────────────────────────────────────────────────
  const uploadFile = async (file, replace = false) => {
    if (!file) return;
    if (file.size > 20 * 1024 * 1024) { alert('File exceeds 20 MB limit.'); return; }

    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf', 'docx', 'txt', 'md'].includes(ext)) {
      alert('Supported formats: PDF, DOCX, TXT, MD.'); return;
    }

    setIsUploading(true);
    flash(`Uploading and indexing "${file.name}"…`);

    const form = new FormData();
    form.append('file', file);
    form.append('session_id', sessionId);
    form.append('replace', replace ? 'true' : 'false');

    try {
      const r = await fetch(`${API_BASE}/documents/`, { method: 'POST', body: form });
      const d = await r.json();
      if (r.ok) {
        setDocument(d.document);
        if (replace) setMessages([]);
        flash(`"${file.name}" indexed — ${d.chunk_count} chunks ready!`);
      } else {
        alert(d.error || 'Upload failed.');
      }
    } catch { alert('Network error during upload.'); }
    finally { setIsUploading(false); }
  };

  const onFileChange = (e) => {
    const file = e.target.files[0]; if (!file) return;
    if (document) { setPendingFile(file); setConfirmReplace(true); }
    else uploadFile(file);
    e.target.value = '';
  };

  const onDrop = (e) => {
    e.preventDefault(); setIsDragging(false);
    const file = e.dataTransfer.files[0]; if (!file) return;
    if (document) { setPendingFile(file); setConfirmReplace(true); }
    else uploadFile(file);
  };

  // ─── Remove document ─────────────────────────────────────────────────────
  const removeDoc = async () => {
    if (!document || !window.confirm('Remove document? Chat will reset.')) return;
    try {
      await fetch(`${API_BASE}/documents/${document.id}/`, { method: 'DELETE' });
      setDocument(null); setMessages([]);
    } catch { alert('Failed to remove.'); }
  };

  // ─── Quick Action (Summarize / Key Points / Outline / Entities) ──────────
  const runAction = async (actionId) => {
    if (!document || runningAction || isAnswering) return;
    setRunningAction(actionId);

    const actionDef = DOC_ACTIONS.find(a => a.id === actionId);
    const userMsg = {
      id: 'act_' + Date.now(), role: 'user',
      content: `📌 ${actionDef?.label || actionId}: ${actionDef?.desc || ''}`,
      created_at: new Date().toISOString(), isAction: true
    };
    setMessages(prev => [...prev, userMsg]);

    try {
      const r = await fetch(`${API_BASE}/documents/${document.id}/actions/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: actionId, session_id: sessionId, api_key: apiKey || undefined })
      });
      const d = await r.json();
      if (r.ok) {
        setMessages(prev => [...prev, {
          id: 'asr_' + Date.now(), role: 'assistant',
          content: d.answer, sources: d.sources || [],
          engine: d.engine, declined: false,
          created_at: new Date().toISOString()
        }]);
      } else {
        setMessages(prev => [...prev, {
          id: 'err_' + Date.now(), role: 'assistant',
          content: d.error || 'Action failed.', sources: [],
          declined: true, created_at: new Date().toISOString()
        }]);
      }
    } catch {
      setMessages(prev => [...prev, {
        id: 'err_' + Date.now(), role: 'assistant',
        content: 'Could not connect to backend.', sources: [],
        declined: true, created_at: new Date().toISOString()
      }]);
    } finally { setRunningAction(null); }
  };

  // ─── Send chat question ───────────────────────────────────────────────────
  const sendMessage = async (text) => {
    const q = (text || query).trim();
    if (!q || !document || isAnswering || runningAction) return;
    if (q.length > 2000) { alert('Message exceeds 2000 characters.'); return; }

    setMessages(prev => [...prev, {
      id: 'u_' + Date.now(), role: 'user', content: q, created_at: new Date().toISOString()
    }]);
    setQuery(''); setIsAnswering(true);

    try {
      const r = await fetch(`${API_BASE}/chat/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, query: q, api_key: apiKey || undefined })
      });
      const d = await r.json();
      setMessages(prev => [...prev, {
        id: d.message_id || 'a_' + Date.now(), role: 'assistant',
        content: r.ok ? d.answer : (d.error || 'Error.'),
        sources: r.ok ? (d.sources || []) : [],
        engine: d.engine, declined: d.declined,
        created_at: new Date().toISOString()
      }]);
    } catch {
      setMessages(prev => [...prev, {
        id: 'err_' + Date.now(), role: 'assistant',
        content: 'Cannot reach Django server. Is it running on port 8000?',
        sources: [], declined: true, created_at: new Date().toISOString()
      }]);
    } finally { setIsAnswering(false); }
  };

  // ─── Clear chat ───────────────────────────────────────────────────────────
  const clearChat = async () => {
    if (!messages.length || !window.confirm('Clear conversation? Document remains.')) return;
    try { await fetch(`${API_BASE}/chat/${sessionId}/`, { method: 'DELETE' }); setMessages([]); }
    catch { alert('Failed to clear.'); }
  };

  // ─── Copy ─────────────────────────────────────────────────────────────────
  const copyMsg = (text, idx) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  // ─── Settings save ────────────────────────────────────────────────────────
  const saveSettings = async () => {
    const r = await fetch(`${API_BASE}/settings/`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key: apiKey, model_name: modelName, temperature: parseFloat(temperature) })
    });
    const d = await r.json();
    if (r.ok) { setHasApiKey(d.has_api_key); setSettingsOpen(false); flash('Settings saved!'); }
  };

  const fmtSize = (b) => {
    if (!b) return '';
    const k = 1024, s = ['B', 'KB', 'MB'];
    const i = Math.floor(Math.log(b) / Math.log(k));
    return (b / Math.pow(k, i)).toFixed(1) + ' ' + s[i];
  };

  const fmtTime = (iso) => new Date(iso || Date.now()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  // ─── Suggested questions (generic, works for any doc) ────────────────────
  const genericSuggestions = [
    'Summarize this document',
    'What are the key points?',
    'Give me an outline of this document',
    'What is the main topic discussed?',
    'Extract all important names and dates',
    'What conclusions does the document reach?',
    'List all rules or requirements mentioned',
  ];

  // ─── Render ───────────────────────────────────────────────────────────────
  return (
    <div className="app-container">

      {/* ── Header ────────────────────────────────────────────────────────── */}
      <header className="app-header">
        <div className="header-left">
          <div className="logo-badge"><BookOpen size={20} /></div>
          <div>
            <h1 className="brand-title">Document Q&amp;A</h1>
            <p className="brand-sub">Upload any document · Summarize · Q&amp;A · Extract</p>
          </div>
        </div>
        <div className="header-center">
          <div className="badge-tag gemini"><Sparkles size={12} />{modelName}</div>
          <div className="badge-tag guardrail"><ShieldCheck size={12} />Guardrails Active</div>
        </div>
        <div className="header-right">
          {messages.length > 0 && (
            <button className="btn-header" onClick={() => {
              const txt = messages.map(m => `[${m.role.toUpperCase()}] ${m.content}`).join('\n\n');
              const a = Object.assign(document.createElement('a'), {
                href: URL.createObjectURL(new Blob([txt], { type: 'text/plain' })),
                download: 'chat_export.txt'
              });
              a.click();
            }}>
              <Download size={13} /> Export
            </button>
          )}
          <button className="btn-header" onClick={() => setSettingsOpen(true)}>
            <SettingsIcon size={13} /> Settings{hasApiKey ? ' ✓' : ''}
          </button>
        </div>
      </header>

      {/* ── Status toast ──────────────────────────────────────────────────── */}
      {statusMsg && (
        <div className="status-toast fade-in">
          <CheckCircle2 size={14} /> {statusMsg}
        </div>
      )}

      {/* ── Main layout ───────────────────────────────────────────────────── */}
      <div className="main-layout">

        {/* ── Left panel ────────────────────────────────────────────────── */}
        <aside className="doc-panel">

          {/* Upload Zone */}
          <div>
            <p className="panel-section-title">📁 Document</p>
            {!document ? (
              <div
                className={`upload-card ${isDragging ? 'drag-active' : ''}`}
                onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={onDrop}
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="upload-icon"><Upload size={22} /></div>
                <div className="upload-text">Drop or click to upload</div>
                <div className="upload-sub">PDF · DOCX · TXT · MD &nbsp;up to 20 MB</div>
                <input ref={fileInputRef} type="file" accept=".pdf,.docx,.txt,.md"
                  style={{ display: 'none' }} onChange={onFileChange} />
              </div>
            ) : (
              <div className="active-doc-card fade-in">
                <div className="doc-card-header">
                  <div className="doc-type-icon"><FileText size={20} /></div>
                  <div className="doc-info">
                    <h3 className="doc-name" title={document.filename}>{document.filename}</h3>
                    <div className="doc-meta">
                      <span style={{ color: '#059669', fontWeight: 700 }}>● Ready</span>
                      <span>·</span><span>{fmtSize(document.file_size)}</span>
                      <span>·</span><span>{document.page_count} pages</span>
                    </div>
                  </div>
                </div>

                {/* Quick Action Buttons */}
                <div className="actions-grid">
                  {DOC_ACTIONS.map(a => {
                    const Icon = a.icon;
                    const busy = runningAction === a.id;
                    return (
                      <button
                        key={a.id}
                        className="action-btn"
                        style={{ '--action-color': a.color, '--action-bg': a.bg }}
                        onClick={() => runAction(a.id)}
                        disabled={!!runningAction || isAnswering}
                        title={a.desc}
                      >
                        {busy ? <RefreshCw size={14} className="pulse" /> : <Icon size={14} />}
                        <span>{a.label}</span>
                      </button>
                    );
                  })}
                </div>

                <div className="doc-card-actions">
                  <button className="btn-doc-action" onClick={() => fileInputRef.current?.click()}>
                    <FileInput size={12} /> Replace
                    <input ref={fileInputRef} type="file" accept=".pdf,.docx,.txt,.md"
                      style={{ display: 'none' }} onChange={onFileChange} />
                  </button>
                  <button className="btn-doc-action danger" onClick={removeDoc}>
                    <Trash2 size={12} /> Remove
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* College Policy Shortcut */}
          {showPolicyCard && (
            <div className="college-policy-card fade-in">
              <button className="policy-close" onClick={() => setShowPolicyCard(false)}><X size={13} /></button>
              <div className="policy-badge">Built-in Sample</div>
              <h2 className="policy-card-title">Meridian College Policy Manual</h2>
              <p className="policy-card-desc">12-page institutional policy PDF — load instantly to try the chatbot.</p>
              <button className="btn-load-policy" onClick={() => loadPolicy()} disabled={isUploading}>
                <Plus size={13} />
                {isUploading ? 'Loading…' : 'Load Policy PDF'}
              </button>
            </div>
          )}

          {/* Guardrails info */}
          <div className="guardrails-card">
            <div className="guardrails-title"><ShieldCheck size={14} color="#2563eb" /> SRS Behaviour Rules</div>
            <ul className="guardrails-list">
              <li>• Answers only from the uploaded document</li>
              <li>• Declines off-topic or general knowledge queries</li>
              <li>• Blocks prompt injection attempts</li>
              <li>• Cites page numbers and section headings</li>
              <li>• Low temperature (0.2) — no hallucinations</li>
            </ul>
          </div>
        </aside>

        {/* ── Chat panel ────────────────────────────────────────────────── */}
        <main className="chat-panel">

          {/* Chat header */}
          <div className="chat-header">
            <div className="chat-header-title">
              {document
                ? <><FileText size={15} color="#2563eb" /> {document.filename}</>
                : <><BookOpen size={15} color="#94a3b8" /> No document loaded</>
              }
            </div>
            {messages.length > 0 && (
              <button className="btn-header" onClick={clearChat}><Trash2 size={12} /> Clear</button>
            )}
          </div>

          {/* Messages */}
          <div className="messages-container">
            {messages.length === 0 ? (
              <div className="chat-empty-state fade-in">
                <div className="empty-icon-box">
                  {document ? <Search size={28} /> : <Upload size={28} />}
                </div>
                <h3 className="empty-title">
                  {document ? `Ask anything about "${document.filename}"` : 'Upload a document to begin'}
                </h3>
                <p className="empty-desc">
                  {document
                    ? 'Use the action buttons above for one-click summaries, key points, outlines and entity extraction — or type any custom question below.'
                    : 'Drop a PDF, DOCX, or TXT file on the left panel, or load the built-in College Policy Manual to get started.'
                  }
                </p>
                {document && (
                  <div className="suggested-section">
                    <span className="suggested-label">Try asking</span>
                    <div className="suggested-pills">
                      {genericSuggestions.map((q, i) => (
                        <button key={i} className="suggested-pill" onClick={() => sendMessage(q)}>{q}</button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div key={msg.id || idx} className={`message-row ${msg.role} fade-in`}>
                  <div className="msg-avatar">
                    {msg.role === 'user' ? 'U' : 'AI'}
                  </div>
                  <div className="msg-content-wrapper">
                    <div className={`msg-bubble ${msg.isAction ? 'action-bubble' : ''}`}>
                      {msg.content}

                      {/* Source citations */}
                      {msg.sources?.length > 0 && (
                        <div className="sources-card">
                          <div className="sources-header"
                            onClick={() => setExpandedSources(p => ({ ...p, [idx]: !p[idx] }))}>
                            <span>📚 {msg.sources.length} source{msg.sources.length > 1 ? 's' : ''} cited</span>
                            {expandedSources[idx] ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
                          </div>
                          {expandedSources[idx] && (
                            <div className="sources-list fade-in">
                              {msg.sources.map((s, si) => (
                                <div key={si} className="source-item">
                                  <span className="source-page-badge">Page {s.page}</span>
                                  <strong>{s.heading}</strong>
                                  <p className="source-text">"{s.text}"</p>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    <div className="msg-meta">
                      <span>{fmtTime(msg.created_at)}</span>
                      {msg.role === 'assistant' && (
                        <><span>·</span>
                        <span style={{ color: msg.declined ? '#f97316' : '#10b981' }}>
                          {msg.declined ? 'Declined' : (msg.engine === 'gemini' ? 'Gemini API' : 'Grounded')}
                        </span></>
                      )}
                    </div>

                    {msg.role === 'assistant' && (
                      <div className="msg-actions">
                        <button className="btn-msg-action" onClick={() => copyMsg(msg.content, idx)}>
                          {copiedIndex === idx ? <Check size={11} color="#10b981" /> : <Copy size={11} />}
                          <span>{copiedIndex === idx ? 'Copied' : 'Copy'}</span>
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}

            {/* Thinking indicator */}
            {(isAnswering || runningAction) && (
              <div className="message-row assistant fade-in">
                <div className="msg-avatar">AI</div>
                <div className="msg-content-wrapper">
                  <div className="msg-bubble" style={{ display: 'flex', gap: 8, color: '#64748b', alignItems: 'center' }}>
                    <RefreshCw size={14} className="pulse" />
                    {runningAction
                      ? `Running "${DOC_ACTIONS.find(a => a.id === runningAction)?.label}" on document…`
                      : 'Searching passages and generating grounded response…'
                    }
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input bar */}
          <div className="chat-input-area">
            <div className={`input-box-wrapper ${!document ? 'disabled' : ''}`}>
              <textarea
                className="chat-textarea"
                placeholder={
                  document
                    ? 'Ask anything about this document… (Enter to send, Shift+Enter for new line)'
                    : 'Upload a document first to start the conversation.'
                }
                value={query}
                onChange={e => setQuery(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } }}
                disabled={!document || isAnswering || !!runningAction}
                maxLength={2000}
                rows={1}
              />
              <div className="input-bottom-bar">
                <span className="input-hint">
                  {!document && <span style={{ color: '#ef4444' }}>⚠ Document required</span>}
                  {document && <span>Strictly grounded in document · Temperature {temperature}</span>}
                </span>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span className="char-counter">{query.length}/2000</span>
                  <button className="btn-send"
                    onClick={() => sendMessage()}
                    disabled={!document || !query.trim() || isAnswering || !!runningAction}>
                    <Send size={14} />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* ── Confirm Replace Modal ─────────────────────────────────────────── */}
      {confirmReplace && (
        <div className="modal-backdrop">
          <div className="modal-content fade-in" style={{ maxWidth: 420 }}>
            <div className="modal-header">
              <h3 className="modal-title">Replace current document?</h3>
            </div>
            <div className="modal-body">
              <p style={{ fontSize: '0.9rem', color: '#475569' }}>
                Uploading <strong>"{pendingFile?.name}"</strong> will replace <strong>"{document?.filename}"</strong> and reset the conversation.
              </p>
            </div>
            <div className="modal-footer">
              <button className="btn-header" onClick={() => { setConfirmReplace(false); setPendingFile(null); }}>Cancel</button>
              <button className="btn-header primary" onClick={() => { setConfirmReplace(false); if (pendingFile) uploadFile(pendingFile, true); setPendingFile(null); }}>
                Yes, Replace
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ── Settings Modal ────────────────────────────────────────────────── */}
      {settingsOpen && (
        <div className="modal-backdrop">
          <div className="modal-content fade-in">
            <div className="modal-header">
              <h3 className="modal-title">Configuration</h3>
              <button className="btn-header" onClick={() => setSettingsOpen(false)}><X size={15} /></button>
            </div>
            <div className="modal-body">
              <div className="form-group">
                <label className="form-label">Google Gemini API Key</label>
                <input type="password" className="form-input"
                  placeholder={hasApiKey ? 'Configured — enter new key to update' : 'AIzaSy…'}
                  value={apiKey} onChange={e => setApiKey(e.target.value)} />
                <span className="form-sub">Get your key at <a href="https://aistudio.google.com/" target="_blank" rel="noreferrer">aistudio.google.com</a>. When absent, the built-in grounded engine is used.</span>
              </div>
              <div className="form-group">
                <label className="form-label">Model</label>
                <select className="form-select" value={modelName} onChange={e => setModelName(e.target.value)}>
                  <option value="gemini-2.5-flash">Gemini 2.5 Flash (Recommended)</option>
                  <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
                  <option value="gemini-2.0-flash">Gemini 2.0 Flash</option>
                  <option value="gemini-2.5-pro">Gemini 2.5 Pro</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Temperature: {temperature}</label>
                <input type="range" min="0" max="0.5" step="0.05" value={temperature}
                  onChange={e => setTemperature(e.target.value)} />
                <span className="form-sub">Keep at 0.2 or lower for strict document grounding.</span>
              </div>
              <div className="form-group">
                <label className="form-label">System Prompt (SRS v1.0)</label>
                <div className="code-preview">{sysPrompt}</div>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn-header" onClick={() => setSettingsOpen(false)}>Cancel</button>
              <button className="btn-header primary" onClick={saveSettings}>Save</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
