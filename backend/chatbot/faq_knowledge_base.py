"""
FAQ Knowledge Base — Education Domain
Smart India Hackathon 2025 — Problem Statement 25104

Contains 50+ Q&A pairs across categories:
- Admissions
- Scholarships
- Hostel
- Attendance
- Examinations
- Library
- Placements
- Fees
- Leave
- Faculty
- Canteen
- Sports
- General
"""

# The FAQ database is a list of dicts.
# Each entry has:
#   - intent:    matches Rasa NLU intent name
#   - patterns:  keywords/phrases Rasa would be trained on
#   - answer:    the response to return

FAQ_DATABASE = [

    # ── ADMISSIONS ───────────────────────────────────────────────────────────
    {
        "intent": "ask_admission_process",
        "answer": "Admissions are done through a centralized entrance exam. "
                  "Fill the online application form, appear for the exam, "
                  "and attend the counselling session. Merit list is published on the portal."
    },
    {
        "intent": "ask_admission_deadline",
        "answer": "The admission deadline for this academic year is July 31st. "
                  "Late applications are not accepted after this date."
    },
    {
        "intent": "ask_admission_eligibility",
        "answer": "To be eligible for admission, you must have passed 10+2 "
                  "with at least 60% marks in Physics, Chemistry, and Mathematics."
    },
    {
        "intent": "ask_admission_documents",
        "answer": "Required documents: 10th marksheet, 12th marksheet, "
                  "entrance exam scorecard, birth certificate, caste certificate (if applicable), "
                  "and 4 passport-size photographs."
    },
    {
        "intent": "ask_admission_status",
        "answer": "You can check your admission status by logging into the student portal "
                  "at portal.college.edu and entering your application number."
    },

    # ── SCHOLARSHIPS ─────────────────────────────────────────────────────────
    {
        "intent": "ask_scholarship_available",
        "answer": "We offer Merit Scholarship, Need-based Scholarship, "
                  "SC/ST Scholarship, and the National Talent Scholarship. "
                  "Apply through the scholarship portal before August 15th."
    },
    {
        "intent": "ask_scholarship_merit",
        "answer": "Merit Scholarship is awarded to students who score above 85% "
                  "in their semester exams. It covers 50% of tuition fees."
    },
    {
        "intent": "ask_scholarship_amount",
        "answer": "Scholarship amounts vary: Merit Scholarship covers ₹25,000/year, "
                  "Need-based covers ₹15,000/year, and Government scholarships follow state rules."
    },
    {
        "intent": "ask_scholarship_apply",
        "answer": "Apply for scholarships through the college portal under the "
                  "'Scholarships' section. Attach income certificate, marksheets, "
                  "and a recommendation letter from HOD."
    },

    # ── HOSTEL ───────────────────────────────────────────────────────────────
    {
        "intent": "ask_hostel_available",
        "answer": "The college provides separate hostels for boys and girls. "
                  "Capacity is 500 for boys and 300 for girls. Apply early as seats are limited."
    },
    {
        "intent": "ask_hostel_fees",
        "answer": "Hostel fees are ₹40,000 per year including meals. "
                  "Room-only accommodation is ₹25,000 per year."
    },
    {
        "intent": "ask_hostel_rules",
        "answer": "Hostel gates close at 10 PM. No visitors after 8 PM. "
                  "Alcohol and smoking are strictly prohibited. "
                  "Quiet hours are 10 PM to 6 AM."
    },
    {
        "intent": "ask_hostel_apply",
        "answer": "Submit the hostel application form to the Hostel Warden's Office "
                  "by July 15th. Preference is given to outstation students."
    },
    {
        "intent": "ask_hostel_facilities",
        "answer": "Hostel facilities include Wi-Fi, laundry, a common room with TV, "
                  "24-hour water supply, and a mess with home-cooked meals."
    },

    # ── ATTENDANCE ───────────────────────────────────────────────────────────
    {
        "intent": "ask_attendance_required",
        "answer": "A minimum of 75% attendance is required in each subject "
                  "to be eligible for semester examinations."
    },
    {
        "intent": "ask_attendance_shortage",
        "answer": "If your attendance falls below 75%, you will receive a warning letter. "
                  "Below 65%, you will be detained and cannot sit for exams."
    },
    {
        "intent": "ask_attendance_condonation",
        "answer": "Attendance condonation is granted only for medical emergencies "
                  "with valid hospital documents. Apply to the HOD within 7 days of rejoining."
    },
    {
        "intent": "ask_attendance_check",
        "answer": "You can check your attendance on the student portal under "
                  "'My Attendance'. It is updated every week by faculty."
    },

    # ── EXAMINATIONS ─────────────────────────────────────────────────────────
    {
        "intent": "ask_exam_schedule",
        "answer": "Semester exams are held in November (odd semester) and April (even semester). "
                  "The exam schedule is published 3 weeks before exams on the notice board."
    },
    {
        "intent": "ask_exam_hall_ticket",
        "answer": "Hall tickets are available on the student portal 10 days before exams. "
                  "You must show your hall ticket and college ID to enter the exam hall."
    },
    {
        "intent": "ask_exam_revaluation",
        "answer": "Revaluation requests can be submitted within 15 days after result declaration. "
                  "The fee is ₹300 per subject. Apply at the Examination Office."
    },
    {
        "intent": "ask_exam_result",
        "answer": "Results are declared within 45 days after the last exam. "
                  "Check results on the official college portal under 'Results'."
    },
    {
        "intent": "ask_exam_backlog",
        "answer": "Supplementary exams for backlog subjects are held 2 months after main results. "
                  "Register through the exam portal and pay ₹500 per subject."
    },
    {
        "intent": "ask_exam_materials",
        "answer": "You are allowed to carry only a pen, pencil, and approved scientific calculator. "
                  "Mobile phones and smartwatches are strictly prohibited."
    },

    # ── LIBRARY ──────────────────────────────────────────────────────────────
    {
        "intent": "ask_library_timing",
        "answer": "The library is open Monday to Saturday from 8 AM to 8 PM. "
                  "It is closed on Sundays and public holidays."
    },
    {
        "intent": "ask_library_books",
        "answer": "Students can borrow up to 3 books for 14 days. "
                  "A fine of ₹2 per day is charged for late returns."
    },
    {
        "intent": "ask_library_membership",
        "answer": "Library membership is automatically given to all enrolled students. "
                  "Use your student ID card to borrow books."
    },
    {
        "intent": "ask_library_ebooks",
        "answer": "The library provides access to NPTEL, IEEE Xplore, and Springer e-books. "
                  "Log in with your college credentials on the library website."
    },

    # ── FEES ─────────────────────────────────────────────────────────────────
    {
        "intent": "ask_fee_structure",
        "answer": "Annual tuition fee: ₹80,000. Exam fee: ₹3,000 per semester. "
                  "Lab fee: ₹5,000 per year. Development fee: ₹2,000 per year."
    },
    {
        "intent": "ask_fee_payment",
        "answer": "Fees can be paid online through the college portal using "
                  "UPI, Net Banking, or Credit/Debit cards. "
                  "You can also pay at the accounts office by DD."
    },
    {
        "intent": "ask_fee_deadline",
        "answer": "Fee payment deadline for the current semester is August 31st. "
                  "A fine of ₹100 per day is charged after the deadline."
    },
    {
        "intent": "ask_fee_receipt",
        "answer": "Fee receipts are available on the student portal under 'Payments'. "
                  "Download the PDF receipt for your records."
    },
    {
        "intent": "ask_fee_installment",
        "answer": "Fee installment facility is available for students in financial need. "
                  "Submit an installment request to the Accounts Office with parent income proof."
    },

    # ── LEAVE ────────────────────────────────────────────────────────────────
    {
        "intent": "ask_leave_apply",
        "answer": "Apply for leave through the student portal under 'Leave Application'. "
                  "Medical leave requires a doctor's certificate. "
                  "Apply before the leave date when possible."
    },
    {
        "intent": "ask_leave_medical",
        "answer": "Medical leave is granted with a valid medical certificate. "
                  "Submit the certificate within 3 days of rejoining. "
                  "Extended medical leave (>7 days) requires HOD approval."
    },
    {
        "intent": "ask_leave_casual",
        "answer": "Casual leave of up to 2 days per month is allowed. "
                  "Apply through the portal and inform your class teacher in advance."
    },

    # ── PLACEMENTS ───────────────────────────────────────────────────────────
    {
        "intent": "ask_placement_process",
        "answer": "Placement drives are held from October to February. "
                  "Register on the placement portal, attend pre-placement talks, "
                  "and appear for written tests and interviews."
    },
    {
        "intent": "ask_placement_eligibility",
        "answer": "To be eligible for placements, you need a minimum 6.0 CGPA "
                  "and no active backlogs. Some companies require 7.0+ CGPA."
    },
    {
        "intent": "ask_placement_companies",
        "answer": "Top recruiters include TCS, Infosys, Wipro, Cognizant, Accenture, "
                  "Amazon, Microsoft, and many startups. 85% of eligible students get placed."
    },
    {
        "intent": "ask_placement_package",
        "answer": "Average package is ₹6.5 LPA. Highest package last year was ₹24 LPA "
                  "from a product-based company. Median is ₹5.2 LPA."
    },
    {
        "intent": "ask_placement_preparation",
        "answer": "Prepare with aptitude tests, coding challenges, and mock interviews. "
                  "The Training & Placement cell runs workshops every Saturday at 10 AM."
    },

    # ── FACULTY ──────────────────────────────────────────────────────────────
    {
        "intent": "ask_faculty_contact",
        "answer": "Faculty contact details are listed on the college website under 'Faculty'. "
                  "You can also contact faculty during office hours (9 AM to 5 PM on working days)."
    },
    {
        "intent": "ask_faculty_office_hours",
        "answer": "Faculty are available for student consultation from 11 AM to 12 PM "
                  "and 2 PM to 3 PM on Monday, Wednesday, and Friday."
    },
    {
        "intent": "ask_faculty_hod",
        "answer": "The HOD of CSE is Dr. Rajesh Kumar (rajesh@college.edu). "
                  "For ECE, contact Dr. Priya Sharma. For Mechanical, contact Dr. Vikram Singh."
    },

    # ── CANTEEN ──────────────────────────────────────────────────────────────
    {
        "intent": "ask_canteen_timing",
        "answer": "The canteen is open from 8 AM to 6 PM on weekdays "
                  "and 9 AM to 2 PM on Saturdays. It is closed on Sundays."
    },
    {
        "intent": "ask_canteen_menu",
        "answer": "The canteen serves breakfast (idli, dosa, upma), lunch (rice, roti, dal), "
                  "and snacks (samosa, tea, coffee). A full meal costs ₹50."
    },

    # ── SPORTS ───────────────────────────────────────────────────────────────
    {
        "intent": "ask_sports_facilities",
        "answer": "Sports facilities include a cricket ground, football field, basketball court, "
                  "badminton hall, table tennis room, and a gym. All are free for enrolled students."
    },
    {
        "intent": "ask_sports_tryouts",
        "answer": "College sports team tryouts are held in the first week of August. "
                  "Check the notice board for specific timings for each sport."
    },

    # ── GENERAL ──────────────────────────────────────────────────────────────
    {
        "intent": "ask_college_timing",
        "answer": "College hours are 8:30 AM to 4:30 PM, Monday to Saturday. "
                  "The college is closed on Sundays and government holidays."
    },
    {
        "intent": "ask_principal_contact",
        "answer": "The Principal's office can be reached at principal@college.edu "
                  "or by phone at +91-80-12345678. Office hours are 10 AM to 4 PM."
    },
    {
        "intent": "ask_wifi_access",
        "answer": "Wi-Fi is available throughout the campus. "
                  "Connect to 'CollegeNet' and use your student ID and date of birth as password."
    },
    {
        "intent": "ask_tc_bonafide",
        "answer": "Transfer Certificates and Bonafide Certificates are issued by the admin office. "
                  "Submit a written request and collect within 5 working days."
    },
    {
        "intent": "ask_internship",
        "answer": "Internship registrations are open from January to March. "
                  "You can pursue internships during summer vacations (May-June). "
                  "Get approval from your HOD before joining."
    },
    {
        "intent": "ask_anti_ragging",
        "answer": "Ragging is strictly prohibited. Report any incidents to the "
                  "Anti-Ragging Committee at antiragging@college.edu or call the helpline 1800-180-5522."
    },


    # ── GREETINGS ─────────────────────────────────────────────────────────────
    {
        "intent": "greet",
        "answer": "Hello! 👋 Welcome to the College Information Chatbot. "
                  "I can help you with questions about Admissions, Fees, Hostel, "
                  "Exams, Scholarships, Placements, Library, Attendance, and more. "
                  "What would you like to know?"
    },

    # ── FALLBACK ─────────────────────────────────────────────────────────────
    {
        "intent": "unknown",
        "answer": "I'm sorry, I don't have information on that topic. "
                  "Please contact the college admin at admin@college.edu or visit the front office."
    },
]

# Build a quick lookup dictionary: intent → answer
FAQ_LOOKUP = {item["intent"]: item["answer"] for item in FAQ_DATABASE}


def get_answer(intent: str) -> str:
    """
    Retrieve the FAQ answer for a given intent.
    Falls back to the 'unknown' answer if intent not found.
    """
    return FAQ_LOOKUP.get(intent, FAQ_LOOKUP["unknown"])
