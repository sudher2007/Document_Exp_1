import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_policy_pdf(output_path="meridian_college_policy_manual.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=1, # Center
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#b45309'),
        alignment=1,
        spaceAfter=8
    )

    desc_style = ParagraphStyle(
        'DocDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#374151'),
        alignment=1,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'SecH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=10,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'SecH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1f2937'),
        spaceBefore=6,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#111827')
    )

    story = []

    # PAGE 1: Title & Document Details
    story.append(Spacer(1, 120))
    story.append(Paragraph("MERIDIAN COLLEGE OF ARTS AND SCIENCE", title_style))
    story.append(Paragraph("Institutional Policy Manual", subtitle_style))
    story.append(Paragraph("Academic, Administrative, Student Welfare and Governance Policies", desc_style))
    story.append(Spacer(1, 40))

    doc_details_data = [
        [Paragraph("<b>Document Details</b>", table_header_style), Paragraph("", table_header_style)],
        [Paragraph("<b>Edition</b>", table_cell_style), Paragraph("First Edition, Academic Year 2026-27", table_cell_style)],
        [Paragraph("<b>Effective From</b>", table_cell_style), Paragraph("1 June 2026", table_cell_style)],
        [Paragraph("<b>Approved By</b>", table_cell_style), Paragraph("Governing Council and Academic Council", table_cell_style)],
        [Paragraph("<b>Review Cycle</b>", table_cell_style), Paragraph("Every two years, or earlier if regulations change", table_cell_style)],
        [Paragraph("<b>Note</b>", table_cell_style), Paragraph("Meridian College is an imaginary institution. Policies are modelled on common practices of Indian arts and science colleges and university/UGC-style norms. Adapt before real-world use.", table_cell_style)],
    ]
    t1 = Table(doc_details_data, colWidths=[140, 380])
    t1.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t1)
    story.append(PageBreak())

    # PAGE 2: Table of Contents
    story.append(Paragraph("Table of Contents", h1_style))
    story.append(Spacer(1, 10))
    toc_items = [
        "1. Vision, Mission and Scope",
        "2. Admission Policy",
        "3. Academic Policy",
        "4. Examination and Assessment Policy",
        "5. Academic Integrity Policy",
        "6. Student Code of Conduct and Discipline",
        "7. Anti-Ragging Policy",
        "8. Prevention of Sexual Harassment Policy",
        "9. Fee, Refund and Scholarship Policy",
        "10. Library Policy",
        "11. IT and Acceptable Use Policy",
        "12. Hostel Policy",
        "13. Transport Policy",
        "14. Health, Safety and Emergency Policy",
        "15. Equal Opportunity and Inclusion Policy",
        "16. Grievance Redressal Policy",
        "17. Placement and Career Services Policy",
        "18. Faculty and Staff Conduct Policy",
        "19. Research and Ethics Policy",
        "20. Data Privacy and Records Policy",
        "21. Environmental Sustainability Policy",
        "22. Amendment and Interpretation",
        "Appendix: Key Contacts and Committees"
    ]
    for item in toc_items:
        story.append(Paragraph(item, body_style))
    story.append(PageBreak())

    # PAGE 3: Vision, Mission & Admission Policy
    story.append(Paragraph("1. Vision, Mission and Scope", h1_style))
    story.append(Paragraph("1.1 Vision", h2_style))
    story.append(Paragraph("To be a respected centre of learning that develops knowledgeable, ethical and socially responsible graduates.", body_style))
    story.append(Paragraph("1.2 Mission", h2_style))
    story.append(Paragraph("• Provide quality undergraduate and postgraduate education in arts, science and commerce.", bullet_style))
    story.append(Paragraph("• Encourage inquiry, creativity, research and community engagement.", bullet_style))
    story.append(Paragraph("• Maintain a safe, inclusive and respectful campus for every member.", bullet_style))
    story.append(Paragraph("1.3 Scope", h2_style))
    story.append(Paragraph("These policies apply to all students, faculty, non-teaching staff, contract workers, visitors and vendors on campus, at college-organised events and on college digital platforms. The Principal is the final executive authority, acting on the advice of the Governing Council and relevant committees.", body_style))
    story.append(Paragraph("1.4 Core Values", h2_style))
    story.append(Paragraph("• Integrity and honesty", bullet_style))
    story.append(Paragraph("• Respect and inclusion", bullet_style))
    story.append(Paragraph("• Accountability and transparency", bullet_style))
    story.append(Paragraph("• Excellence and continuous improvement", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Admission Policy", h1_style))
    story.append(Paragraph("2.1 Principles", h2_style))
    story.append(Paragraph("Admissions are merit-based, transparent and non-discriminatory, in line with the affiliating university norms and government reservation rules.", body_style))
    story.append(Paragraph("2.2 Eligibility", h2_style))
    story.append(Paragraph("• UG programmes: pass in Higher Secondary (10+2) or equivalent from a recognised board, with subject requirements specified per programme.", bullet_style))
    story.append(Paragraph("• PG programmes: a bachelor's degree from a recognised university with the minimum marks stated in the prospectus.", bullet_style))
    story.append(Paragraph("• Lateral entry and transfer admissions are allowed only where the affiliating university permits and seats are available.", bullet_style))
    story.append(Paragraph("2.3 Seat Matrix and Reservation", h2_style))
    seat_data = [
        [Paragraph("<b>Category</b>", table_header_style), Paragraph("<b>Policy</b>", table_header_style)],
        [Paragraph("Reserved categories", table_cell_style), Paragraph("As per applicable State and Central Government rules", table_cell_style)],
        [Paragraph("Persons with disabilities", table_cell_style), Paragraph("Reservation as per the Rights of Persons with Disabilities Act, 2016", table_cell_style)],
        [Paragraph("Sports and extracurricular quota", table_cell_style), Paragraph("Up to 5% of seats, on verified achievements", table_cell_style)],
        [Paragraph("Management quota", table_cell_style), Paragraph("Up to 15% where permitted, filled on merit with published criteria", table_cell_style)],
    ]
    t_seat = Table(seat_data, colWidths=[180, 340])
    t_seat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_seat)
    story.append(PageBreak())

    # PAGE 4: Admission 2.4 - Academic Policy 3.5
    story.append(Paragraph("2.4 Process", h2_style))
    story.append(Paragraph("• Online application with a non-refundable application fee.", bullet_style))
    story.append(Paragraph("• Merit list published on the website; counselling and document verification follow.", bullet_style))
    story.append(Paragraph("• Original certificates are verified at admission; false documents lead to cancellation of admission without refund.", bullet_style))
    story.append(Paragraph("2.5 Cancellation and Withdrawal", h2_style))
    story.append(Paragraph("Withdrawal rules and fee refunds follow Section 9. Withdrawn seats are re-offered to the waiting list until the cut-off date set by the Admission Committee.", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. Academic Policy", h1_style))
    story.append(Paragraph("3.1 Academic Calendar", h2_style))
    story.append(Paragraph("Two semesters a year (odd: June-November, even: December-April). The calendar is published before the start of the year and includes at least 90 instructional days per semester.", body_style))
    story.append(Paragraph("3.2 Curriculum", h2_style))
    story.append(Paragraph("Programmes follow a Choice Based Credit System (CBCS) aligned to the affiliating university and the National Education Policy 2020 framework, including core, elective, skill-enhancement, ability-enhancement and value-added courses.", body_style))
    story.append(Paragraph("3.3 Attendance", h2_style))
    att_data = [
        [Paragraph("<b>Attendance</b>", table_header_style), Paragraph("<b>Consequence</b>", table_header_style)],
        [Paragraph("75% and above", table_cell_style), Paragraph("Eligible to appear for end-semester examinations", table_cell_style)],
        [Paragraph("65% to below 75%", table_cell_style), Paragraph("Condonation possible with valid reasons, medical certificate and payment of condonation fee", table_cell_style)],
        [Paragraph("Below 65%", table_cell_style), Paragraph("Not eligible; the student must repeat the semester or course as per university rules", table_cell_style)],
    ]
    t_att = Table(att_data, colWidths=[150, 370])
    t_att.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_att)
    story.append(Spacer(1, 4))
    story.append(Paragraph("• Up to 10% additional attendance credit may be given for official representation in sports, NCC, NSS and cultural events.", bullet_style))
    story.append(Paragraph("• Leave must be applied for in advance through the mentor and the Head of Department, except in emergencies.", bullet_style))
    story.append(Paragraph("3.4 Mentoring", h2_style))
    story.append(Paragraph("Every student is assigned a faculty mentor who monitors attendance, performance and well-being, and meets the student at least once a month.", body_style))
    story.append(Paragraph("3.5 Grading", h2_style))
    grade_data_p4 = [
        [Paragraph("<b>Marks (%)</b>", table_header_style), Paragraph("<b>Grade</b>", table_header_style), Paragraph("<b>Grade Points</b>", table_header_style)],
        [Paragraph("90-100", table_cell_style), Paragraph("O (Outstanding)", table_cell_style), Paragraph("10", table_cell_style)],
        [Paragraph("80-89", table_cell_style), Paragraph("A+ (Excellent)", table_cell_style), Paragraph("9", table_cell_style)],
        [Paragraph("70-79", table_cell_style), Paragraph("A (Very Good)", table_cell_style), Paragraph("8", table_cell_style)],
        [Paragraph("60-69", table_cell_style), Paragraph("B+ (Good)", table_cell_style), Paragraph("7", table_cell_style)],
    ]
    t_grade_p4 = Table(grade_data_p4, colWidths=[120, 250, 150])
    t_grade_p4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_grade_p4)
    story.append(PageBreak())

    # PAGE 5: Grading continued & Section 4 Examination
    grade_data_p5 = [
        [Paragraph("<b>Marks (%)</b>", table_header_style), Paragraph("<b>Grade</b>", table_header_style), Paragraph("<b>Grade Points</b>", table_header_style)],
        [Paragraph("50-59", table_cell_style), Paragraph("B (Above Average)", table_cell_style), Paragraph("6", table_cell_style)],
        [Paragraph("40-49", table_cell_style), Paragraph("C (Average)", table_cell_style), Paragraph("5", table_cell_style)],
        [Paragraph("Below 40", table_cell_style), Paragraph("F (Fail)", table_cell_style), Paragraph("0", table_cell_style)],
    ]
    t_grade_p5 = Table(grade_data_p5, colWidths=[120, 250, 150])
    t_grade_p5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_grade_p5)
    story.append(Spacer(1, 4))
    story.append(Paragraph("SGPA and CGPA are computed using credit-weighted grade points. A minimum CGPA of 5.0 is needed to be awarded the degree.", body_style))
    story.append(Paragraph("3.6 Progression and Duration", h2_style))
    story.append(Paragraph("UG programmes are completed within the nominal duration plus two years; PG programmes within the nominal duration plus one year. Extensions need the Principal's approval.", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4. Examination and Assessment Policy", h1_style))
    story.append(Paragraph("4.1 Components", h2_style))
    exam_comp_data = [
        [Paragraph("<b>Component</b>", table_header_style), Paragraph("<b>Weightage</b>", table_header_style)],
        [Paragraph("Continuous Internal Assessment (tests, assignments, seminars, attendance)", table_cell_style), Paragraph("25-40% as per course", table_cell_style)],
        [Paragraph("End-Semester Examination", table_cell_style), Paragraph("60-75% as per course", table_cell_style)],
        [Paragraph("Practicals and projects", table_cell_style), Paragraph("As per syllabus", table_cell_style)],
    ]
    t_exam_comp = Table(exam_comp_data, colWidths=[320, 200])
    t_exam_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_exam_comp)
    story.append(Paragraph("4.2 Conduct of Examinations", h2_style))
    story.append(Paragraph("• Students must carry the college ID card and hall ticket.", bullet_style))
    story.append(Paragraph("• Mobile phones, smart watches and unauthorised materials are prohibited in the hall.", bullet_style))
    story.append(Paragraph("• Entry is not permitted after 30 minutes from the start; exit is not permitted in the first 30 minutes.", bullet_style))
    story.append(Paragraph("• Any malpractice is reported to the Examination Malpractice Committee.", bullet_style))
    story.append(Paragraph("4.3 Malpractice Penalties", h2_style))
    malp_data = [
        [Paragraph("<b>Offence</b>", table_header_style), Paragraph("<b>Typical Action</b>", table_header_style)],
        [Paragraph("Possession of unauthorised material", table_cell_style), Paragraph("Cancellation of that paper", table_cell_style)],
        [Paragraph("Copying or helping another candidate", table_cell_style), Paragraph("Cancellation of the semester examination", table_cell_style)],
        [Paragraph("Impersonation or tampering with records", table_cell_style), Paragraph("Debarment for up to two years and possible expulsion", table_cell_style)],
    ]
    t_malp = Table(malp_data, colWidths=[200, 320])
    t_malp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_malp)
    story.append(Paragraph("4.4 Revaluation and Re-totalling", h2_style))
    story.append(Paragraph("Students may apply for photocopies of answer scripts, re-totalling or revaluation within 10 working days of results, on payment of the prescribed fee. Revaluation outcomes are final.", body_style))
    story.append(Paragraph("4.5 Supplementary Examinations and Special Cases", h2_style))
    story.append(Paragraph("Arrear examinations are held with regular examinations. Students with documented medical emergencies or bereavement may apply for a special examination within 15 days.", body_style))
    story.append(Paragraph("5. Academic Integrity Policy", h1_style))
    story.append(PageBreak())

    # PAGE 6: Academic Integrity, Student Conduct, Anti-Ragging intro
    story.append(Paragraph("The college expects originality and honesty in all academic work.", body_style))
    story.append(Paragraph("• Plagiarism, fabrication of data, contract cheating and unauthorised use of generative AI tools in assessments are violations.", bullet_style))
    story.append(Paragraph("• Where AI tools are permitted by the course instructor, use must be declared in the submission.", bullet_style))
    story.append(Paragraph("• Project reports and theses are screened using similarity-detection software; similarity above 20% (excluding references) requires revision.", bullet_style))
    story.append(Paragraph("• First offence: zero marks for the work and a written warning. Repeated offence: course failure and referral to the Disciplinary Committee.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("6. Student Code of Conduct and Discipline", h1_style))
    story.append(Paragraph("6.1 Expected Behaviour", h2_style))
    story.append(Paragraph("• Be punctual, respectful and cooperative with faculty, staff and peers.", bullet_style))
    story.append(Paragraph("• Wear the prescribed uniform or decent attire as notified, and carry the ID card at all times.", bullet_style))
    story.append(Paragraph("• Take care of college property; damage must be compensated.", bullet_style))
    story.append(Paragraph("• Use social media responsibly and never to harass or defame others.", bullet_style))
    story.append(Paragraph("6.2 Prohibited Acts", h2_style))
    story.append(Paragraph("• Possession or use of alcohol, tobacco, narcotics or e-cigarettes on campus.", bullet_style))
    story.append(Paragraph("• Bringing weapons or hazardous materials.", bullet_style))
    story.append(Paragraph("• Gambling, theft, vandalism or physical violence.", bullet_style))
    story.append(Paragraph("• Unauthorised protests, political campaigning or gatherings that disrupt academic work.", bullet_style))
    story.append(Paragraph("• Misuse of the college name or logo.", bullet_style))
    story.append(Paragraph("6.3 Disciplinary Process", h2_style))
    story.append(Paragraph("• A written complaint or report is submitted to the Dean of Student Affairs.", bullet_style))
    story.append(Paragraph("• The student is given a written notice and a fair opportunity to respond.", bullet_style))
    story.append(Paragraph("• The Disciplinary Committee (Dean, two senior faculty, one student representative) hears the case and recommends action.", bullet_style))
    story.append(Paragraph("• The Principal issues the final order; students may appeal to the Governing Council within 15 days.", bullet_style))
    story.append(Paragraph("6.4 Penalties", h2_style))
    pen_data = [
        [Paragraph("<b>Level</b>", table_header_style), Paragraph("<b>Examples of Action</b>", table_header_style)],
        [Paragraph("Minor", table_cell_style), Paragraph("Verbal or written warning, community service, fine", table_cell_style)],
        [Paragraph("Moderate", table_cell_style), Paragraph("Suspension for up to one semester, loss of hostel or transport privileges", table_cell_style)],
        [Paragraph("Severe", table_cell_style), Paragraph("Rustication or expulsion, report to police where required", table_cell_style)],
    ]
    t_pen = Table(pen_data, colWidths=[120, 400])
    t_pen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_pen)
    story.append(Spacer(1, 4))
    story.append(Paragraph("7. Anti-Ragging Policy", h1_style))
    story.append(Paragraph("The college has zero tolerance for ragging, following the directions of the Supreme Court of India and UGC Regulations on Curbing the Menace of Ragging.", body_style))
    story.append(PageBreak())

    # PAGE 7: Anti-Ragging cont, Sexual Harassment, Fee Refund
    story.append(Paragraph("• Ragging in any form, inside or outside campus, is a punishable offence.", bullet_style))
    story.append(Paragraph("• An Anti-Ragging Committee and Anti-Ragging Squad are constituted every year and patrol hostels, canteens and common areas.", bullet_style))
    story.append(Paragraph("• Students and parents submit an anti-ragging undertaking at admission.", bullet_style))
    story.append(Paragraph("• Complaints may be made to the committee, the Principal, the helpline or through the college app, and may be anonymous.", bullet_style))
    story.append(Paragraph("• Penalties include suspension, expulsion, withholding of results and registration of an FIR.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("8. Prevention of Sexual Harassment Policy", h1_style))
    story.append(Paragraph("The college is committed to a campus free from sexual harassment, in line with the Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 and UGC regulations.", body_style))
    story.append(Paragraph("• An Internal Committee (IC), headed by a senior woman faculty member with an external member from an NGO or legal background, handles complaints.", bullet_style))
    story.append(Paragraph("• Complaints may be filed in writing or electronically within three months of the incident (extendable with reason).", bullet_style))
    story.append(Paragraph("• Inquiry is completed within 90 days and confidentiality is strictly maintained.", bullet_style))
    story.append(Paragraph("• Interim relief such as change of class or hostel may be given.", bullet_style))
    story.append(Paragraph("• Retaliation against complainants or witnesses is a separate offence.", bullet_style))
    story.append(Paragraph("• Awareness and sensitisation sessions are held every year for all students and staff.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("9. Fee, Refund and Scholarship Policy", h1_style))
    story.append(Paragraph("9.1 Fee Payment", h2_style))
    story.append(Paragraph("Fees are published annually and are payable per semester by the due date through online payment or the college accounts office. Late payment attracts a fine of Rs. 50 per day up to 15 days, after which the student may be barred from classes and examinations.", body_style))
    story.append(Paragraph("9.2 Refund Schedule (aligned with UGC fee refund norms)", h2_style))
    refund_data = [
        [Paragraph("<b>Time of Withdrawal</b>", table_header_style), Paragraph("<b>Refund of Fees (excluding application fee)</b>", table_header_style)],
        [Paragraph("Up to 15 days before the start of the programme", table_cell_style), Paragraph("100%, less Rs. 1,000 processing fee", table_cell_style)],
        [Paragraph("Up to 15 days after the start of the programme", table_cell_style), Paragraph("90%", table_cell_style)],
        [Paragraph("16 to 30 days after the start", table_cell_style), Paragraph("80%", table_cell_style)],
        [Paragraph("31 to 60 days after the start", table_cell_style), Paragraph("50%", table_cell_style)],
        [Paragraph("After 60 days", table_cell_style), Paragraph("No refund", table_cell_style)],
    ]
    t_ref = Table(refund_data, colWidths=[240, 280])
    t_ref.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_ref)
    story.append(Spacer(1, 4))
    story.append(Paragraph("Caution deposits are refunded after clearing all dues within 30 days of leaving the college.", body_style))
    story.append(Paragraph("9.3 Scholarships and Financial Aid", h2_style))
    story.append(Paragraph("• Government scholarships (SC/ST/OBC/minority and others) are facilitated by the Scholarship Cell.", bullet_style))
    story.append(Paragraph("• Merit scholarships: tuition fee concession for top rankers in each programme, based on previous year's CGPA.", bullet_style))
    story.append(PageBreak())

    # PAGE 8: Scholarships cont, Library, IT, Hostel intro
    story.append(Paragraph("• Need-based aid from the Alumni Fund for students with family income below the limit set by the Scholarship Committee.", bullet_style))
    story.append(Paragraph("• Sports and cultural scholarships for state and national level achievers.", bullet_style))
    story.append(Paragraph("• Scholarships may be withdrawn for poor attendance, misconduct or academic failure.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("10. Library Policy", h1_style))
    story.append(Paragraph("• Open on working days from 8:30 am to 6:00 pm, with extended hours during examinations.", bullet_style))
    story.append(Paragraph("• Undergraduate students may borrow 3 books for 14 days, postgraduate students 5 books for 21 days, and faculty 10 books for one semester.", bullet_style))
    story.append(Paragraph("• Renewal is permitted once if there is no reservation by another member.", bullet_style))
    story.append(Paragraph("• Overdue fine: Rs. 2 per day per book. Lost books must be replaced or paid for at current price plus a processing charge.", bullet_style))
    story.append(Paragraph("• Reference books, journals and rare items are for reading inside the library only.", bullet_style))
    story.append(Paragraph("• Silence must be maintained; food, drinks and phone calls are not permitted.", bullet_style))
    story.append(Paragraph("• E-resources (e-journals, e-books, NPTEL and databases) are accessible through campus network and remote login for registered users.", bullet_style))
    story.append(Paragraph("• Students may recommend titles for purchase through the Library Advisory Committee.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("11. IT and Acceptable Use Policy", h1_style))
    story.append(Paragraph("11.1 Acceptable Use", h2_style))
    story.append(Paragraph("• College computers, Wi-Fi and platforms are for academic and administrative use.", bullet_style))
    story.append(Paragraph("• Users must protect their login credentials and must not share passwords.", bullet_style))
    story.append(Paragraph("• Downloading pirated software, accessing adult or illegal content and hacking attempts are prohibited.", bullet_style))
    story.append(Paragraph("11.2 Security and Monitoring", h2_style))
    story.append(Paragraph("• Network traffic may be monitored for security purposes in line with law.", bullet_style))
    story.append(Paragraph("• Cyber incidents must be reported immediately to the IT Cell.", bullet_style))
    story.append(Paragraph("• Students must not install unauthorised software in laboratory computers.", bullet_style))
    story.append(Paragraph("11.3 Generative AI Use", h2_style))
    story.append(Paragraph("Use of AI tools in coursework is governed by the course instructor's instructions and Section 5. Confidential or personal data must not be entered into public AI services.", body_style))
    story.append(Paragraph("11.4 Violations", h2_style))
    story.append(Paragraph("Violations lead to suspension of IT access, disciplinary action under Section 6 and, where applicable, legal action under the Information Technology Act, 2000.", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("12. Hostel Policy", h1_style))
    story.append(Paragraph("• Separate hostels for men and women, supervised by wardens and resident tutors.", bullet_style))
    story.append(Paragraph("• Admission to the hostel is based on distance from home and availability; seats are allotted yearly.", bullet_style))
    story.append(PageBreak())

    # PAGE 9: Hostel cont, Transport, Health & Safety
    story.append(Paragraph("• Hostel timings: entry before 8:00 pm for first-year students and 9:00 pm for others; late stay requires prior written permission and parent intimation.", bullet_style))
    story.append(Paragraph("• Visitors are allowed only in the visitors' room during notified hours; parents/guardians are registered.", bullet_style))
    story.append(Paragraph("• Prohibited: cooking appliances in rooms, alcohol, tobacco, loud music and overnight guests.", bullet_style))
    story.append(Paragraph("• Room inspections may be done by wardens for safety, with respect for privacy.", bullet_style))
    story.append(Paragraph("• The mess committee (including student members) oversees menu, hygiene and quality; mess fees are shared equally on actual usage basis.", bullet_style))
    story.append(Paragraph("• Damage to hostel property is recovered from the occupants concerned or collectively.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("13. Transport Policy", h1_style))
    story.append(Paragraph("• College buses run on fixed routes; students must register and pay the transport fee for the semester.", bullet_style))
    story.append(Paragraph("• Students must carry the transport pass and board only at designated stops.", bullet_style))
    story.append(Paragraph("• Misbehaviour on buses attracts penalties including suspension of transport privileges.", bullet_style))
    story.append(Paragraph("• Two-wheeler users must hold a valid licence, wear helmets and park in designated areas; speed limit on campus is 20 km/h.", bullet_style))
    story.append(Paragraph("• Vehicle documents are verified at the start of each academic year.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("14. Health, Safety and Emergency Policy", h1_style))
    story.append(Paragraph("14.1 Campus Safety", h2_style))
    story.append(Paragraph("• CCTV coverage at entrances, corridors and parking, with monitored access control.", bullet_style))
    story.append(Paragraph("• Security staff on duty round the clock; visitors must register at the gate.", bullet_style))
    story.append(Paragraph("• Fire extinguishers are inspected quarterly; evacuation drills held twice a year.", bullet_style))
    story.append(Paragraph("• Laboratories follow safety protocols; protective equipment is mandatory.", bullet_style))
    story.append(Paragraph("14.2 Health Services", h2_style))
    story.append(Paragraph("• A medical room with a part-time doctor and nurse, and a tie-up with a nearby hospital for emergencies.", bullet_style))
    story.append(Paragraph("• Students are encouraged to get annual health check-ups; health insurance is recommended.", bullet_style))
    story.append(Paragraph("• First-aid trained volunteers (NSS/Red Cross) are available on campus.", bullet_style))
    story.append(Paragraph("14.3 Mental Health and Wellness", h2_style))
    story.append(Paragraph("A student counselling centre offers free, confidential counselling by qualified professionals, wellness workshops and referrals. Faculty mentors are trained to identify students in distress and refer them with sensitivity.", body_style))
    story.append(Paragraph("14.4 Substance-Free and Smoke-Free Campus", h2_style))
    story.append(Paragraph("The campus is a tobacco-free and drug-free zone in line with applicable laws. Violations are handled under Section 6.", body_style))
    story.append(Paragraph("14.5 Emergency Response", h2_style))
    story.append(Paragraph("A Disaster Management Committee maintains emergency plans for fire, medical emergencies, natural disasters and security threats. Emergency contact numbers are displayed across campus.", body_style))
    story.append(PageBreak())

    # PAGE 10: Equal Opportunity, Grievance, Placement, Faculty intro
    story.append(Paragraph("15. Equal Opportunity and Inclusion Policy", h1_style))
    story.append(Paragraph("• No discrimination on grounds of religion, caste, gender, disability, region, language, economic status or sexual orientation.", bullet_style))
    story.append(Paragraph("• An Equal Opportunity Cell ensures access to scholarships, facilities and academic support for disadvantaged groups.", bullet_style))
    story.append(Paragraph("• Barrier-free campus: ramps, lifts, accessible washrooms and assistive technologies where feasible.", bullet_style))
    story.append(Paragraph("• Students with disabilities receive reasonable accommodations such as extra time, scribes and accessible materials on submitting valid documentation.", bullet_style))
    story.append(Paragraph("• Special cells for SC/ST/OBC, minority and women's welfare monitor representation and grievances.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("16. Grievance Redressal Policy", h1_style))
    story.append(Paragraph("The college provides a fair and timely mechanism for students, parents, faculty and staff to raise concerns.", body_style))
    griev_data = [
        [Paragraph("<b>Level</b>", table_header_style), Paragraph("<b>Authority</b>", table_header_style), Paragraph("<b>Time to Resolve</b>", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("Class mentor or Head of Department", table_cell_style), Paragraph("7 working days", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("Grievance Redressal Committee", table_cell_style), Paragraph("15 working days", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("Principal / Ombudsperson", table_cell_style), Paragraph("30 working days", table_cell_style)],
    ]
    t_griev = Table(griev_data, colWidths=[60, 260, 200])
    t_griev.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_griev)
    story.append(Spacer(1, 4))
    story.append(Paragraph("• Grievances may be submitted by email, the online portal or the physical grievance box.", bullet_style))
    story.append(Paragraph("• Anonymous complaints are accepted for serious concerns such as ragging and harassment.", bullet_style))
    story.append(Paragraph("• Students will not face reprisal for good-faith complaints.", bullet_style))
    story.append(Paragraph("• Appeals beyond the college may be made to the affiliating university or the University Grants Commission as applicable.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("17. Placement and Career Services Policy", h1_style))
    story.append(Paragraph("• The Placement Cell organises training in aptitude, communication and technical skills, plus mock interviews and internships.", bullet_style))
    story.append(Paragraph("• Eligible students are those who have no standing arrears and meet the attendance requirements.", bullet_style))
    story.append(Paragraph("• Students must attend all pre-placement activities; a student who is placed may be restricted from attending further drives except in exceptional cases (such as a significantly better offer), as per Placement Cell rules.", bullet_style))
    story.append(Paragraph("• Students must provide accurate information; misrepresentation leads to being barred from placement.", bullet_style))
    story.append(Paragraph("• Placement data is published annually, including number of offers and salary ranges, in a transparent format.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("18. Faculty and Staff Conduct Policy", h1_style))
    story.append(Paragraph("18.1 Recruitment and Qualifications", h2_style))
    story.append(Paragraph("Faculty are recruited as per UGC qualifications (NET/SLET/Ph.D. as applicable), through a transparent selection committee process.", body_style))
    story.append(Paragraph("18.2 Responsibilities", h2_style))
    story.append(PageBreak())

    # PAGE 11: Faculty resp cont, Leave, Research, Data Privacy
    story.append(Paragraph("• Faculty must complete syllabus coverage, maintain attendance and assessment records and be available for student mentoring.", bullet_style))
    story.append(Paragraph("• A minimum workload as per UGC norms; participation in research, committees and outreach is expected.", bullet_style))
    story.append(Paragraph("• Faculty must declare conflicts of interest and not tutor their own students privately for fees.", bullet_style))
    story.append(Paragraph("18.3 Leave and Service Rules", h2_style))
    leave_data = [
        [Paragraph("<b>Leave Type</b>", table_header_style), Paragraph("<b>Entitlement (per year, indicative)</b>", table_header_style)],
        [Paragraph("Casual leave", table_cell_style), Paragraph("12 days", table_cell_style)],
        [Paragraph("Medical leave", table_cell_style), Paragraph("As per service rules, with certificate", table_cell_style)],
        [Paragraph("Maternity / paternity leave", table_cell_style), Paragraph("As per Government rules", table_cell_style)],
        [Paragraph("Study / duty leave", table_cell_style), Paragraph("On approval for FDPs, conferences and doctoral studies", table_cell_style)],
    ]
    t_leave = Table(leave_data, colWidths=[200, 320])
    t_leave.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_leave)
    story.append(Paragraph("18.4 Performance Appraisal", h2_style))
    story.append(Paragraph("Annual self-appraisal and student feedback (anonymous) inform performance reviews and career advancement. Misconduct is dealt with under the applicable service rules after a fair inquiry.", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("19. Research and Ethics Policy", h1_style))
    story.append(Paragraph("• Faculty and students are encouraged to undertake research, publish in reputed peer-reviewed journals and avoid predatory journals.", bullet_style))
    story.append(Paragraph("• A Research Advisory Committee approves proposals and monitors funded projects.", bullet_style))
    story.append(Paragraph("• Research involving human participants or animals requires ethics committee clearance and informed consent.", bullet_style))
    story.append(Paragraph("• Authorship must reflect actual contributions; honorary authorship is not allowed.", bullet_style))
    story.append(Paragraph("• Intellectual property created with college resources is jointly owned as per the IPR Cell guidelines.", bullet_style))
    story.append(Paragraph("• Research misconduct (fabrication, falsification, plagiarism) is investigated by a committee and penalised.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("20. Data Privacy and Records Policy", h1_style))
    story.append(Paragraph("• Personal data of students and staff is collected only for legitimate academic and administrative purposes and handled in accordance with the Digital Personal Data Protection Act, 2023.", bullet_style))
    story.append(Paragraph("• Access to records is limited to authorised personnel; data is stored securely with regular backups.", bullet_style))
    story.append(Paragraph("• Student academic records are retained permanently; admission and financial records for at least 8 years; CCTV footage for 30-90 days unless needed for an inquiry.", bullet_style))
    story.append(Paragraph("• Photographs and videos of events may be used for official publicity; students may opt out in writing for non-essential uses.", bullet_style))
    story.append(Paragraph("• Data breaches must be reported to the Data Protection Officer within 24 hours of detection.", bullet_style))
    story.append(Paragraph("• Students may request correction of inaccurate personal data through the Registrar's office.", bullet_style))
    story.append(Paragraph("21. Environmental Sustainability Policy", h1_style))
    story.append(PageBreak())

    # PAGE 12: Environmental cont, Amendment, Appendix
    story.append(Paragraph("• Single-use plastics are banned on campus.", bullet_style))
    story.append(Paragraph("• Solar power, LED lighting and water-saving fixtures are used to reduce consumption; an annual green and energy audit is carried out.", bullet_style))
    story.append(Paragraph("• Rainwater harvesting and sewage treatment plants are maintained.", bullet_style))
    story.append(Paragraph("• Waste is segregated into wet, dry and e-waste; e-waste is disposed of through authorised recyclers.", bullet_style))
    story.append(Paragraph("• Green Club and NSS units conduct tree plantation, clean-up drives and awareness events yearly.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("22. Amendment and Interpretation", h1_style))
    story.append(Paragraph("• Policies may be amended by the Governing Council on recommendation of the Academic Council or relevant committees.", bullet_style))
    story.append(Paragraph("• Amendments are communicated through the website and notice boards and apply from the date notified.", bullet_style))
    story.append(Paragraph("• In case of conflict, the regulations of the affiliating university and applicable laws prevail.", bullet_style))
    story.append(Paragraph("• Questions of interpretation are decided by the Principal, whose decision is final subject to the appeal provisions in these policies.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Appendix: Key Contacts and Committees", h1_style))
    app_data = [
        [Paragraph("<b>Committee / Office</b>", table_header_style), Paragraph("<b>Head</b>", table_header_style), Paragraph("<b>Purpose</b>", table_header_style)],
        [Paragraph("Governing Council", table_cell_style), Paragraph("Chairperson", table_cell_style), Paragraph("Policy approval and oversight", table_cell_style)],
        [Paragraph("Academic Council", table_cell_style), Paragraph("Principal", table_cell_style), Paragraph("Curriculum, examinations, academic standards", table_cell_style)],
        [Paragraph("Internal Quality Assurance Cell (IQAC)", table_cell_style), Paragraph("Coordinator", table_cell_style), Paragraph("Quality, accreditation (NAAC/NIRF)", table_cell_style)],
        [Paragraph("Disciplinary Committee", table_cell_style), Paragraph("Dean of Student Affairs", table_cell_style), Paragraph("Student discipline cases", table_cell_style)],
        [Paragraph("Anti-Ragging Committee and Squad", table_cell_style), Paragraph("Principal / Senior Faculty", table_cell_style), Paragraph("Prevention and action on ragging", table_cell_style)],
        [Paragraph("Internal Committee (POSH)", table_cell_style), Paragraph("Presiding Officer", table_cell_style), Paragraph("Sexual harassment complaints", table_cell_style)],
        [Paragraph("Grievance Redressal Committee", table_cell_style), Paragraph("Senior Professor", table_cell_style), Paragraph("Student and staff grievances", table_cell_style)],
        [Paragraph("Equal Opportunity Cell", table_cell_style), Paragraph("Nodal Officer", table_cell_style), Paragraph("Inclusion and accessibility", table_cell_style)],
        [Paragraph("Placement Cell", table_cell_style), Paragraph("Placement Officer", table_cell_style), Paragraph("Career services, internships, recruitment", table_cell_style)],
        [Paragraph("Student Counselling Centre", table_cell_style), Paragraph("Chief Counsellor", table_cell_style), Paragraph("Mental health and wellness", table_cell_style)],
        [Paragraph("IT Cell", table_cell_style), Paragraph("IT Administrator", table_cell_style), Paragraph("Network, cybersecurity, digital services", table_cell_style)],
    ]
    t_app = Table(app_data, colWidths=[150, 130, 240])
    t_app.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_app)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Statutory helplines (for real use):</b> National Anti-Ragging Helpline 1800-180-5522; Women Helpline 181; Emergency 112. Replace placeholder details with the college's own contacts.", body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<i>End of Policy Manual</i>", body_style))

    doc.build(story)
    print(f"Policy PDF generated successfully at {output_path}")

if __name__ == '__main__':
    generate_policy_pdf()
