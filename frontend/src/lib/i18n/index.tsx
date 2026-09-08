"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

type Language = "en" | "hi";

interface Translations {
  [key: string]: {
    en: string;
    hi: string;
  };
}

const translations: Translations = {
  // Navigation
  "nav.brand": { en: "iGOT Karmayogi", hi: "आईगॉट कर्मयोगी" },
  "nav.subBrand": { en: "Official Statistical & Civil Service Learning", hi: "आधिकारिक सांख्यिकी एवं सिविल सेवा शिक्षण" },
  "nav.about": { en: "About", hi: "परिचय" },
  "nav.howItWorks": { en: "How it Works", hi: "यह कैसे कार्य करता है" },
  "nav.resources": { en: "Resources", hi: "संसाधन" },
  "nav.help": { en: "Help", hi: "सहायता" },
  "nav.discover": { en: "Discover", hi: "अन्वेषण करें" },
  "nav.myLearning": { en: "My Learning", hi: "मेरी शिक्षा" },
  "nav.search": { en: "Search Catalogue", hi: "पाठ्यक्रम खोजें" },
  "nav.admin": { en: "Administration", hi: "प्रशासन" },
  "nav.profile": { en: "My Profile", hi: "मेरी प्रोफ़ाइल" },
  "nav.settings": { en: "Settings", hi: "सेटिंग्स" },
  "nav.logout": { en: "Sign Out", hi: "लॉग आउट" },
  "nav.login": { en: "Sign In", hi: "लॉग इन" },
  "nav.register": { en: "Register", hi: "पंजीकरण" },
  "nav.askAi": { en: "Support Desk", hi: "सहायता केंद्र" },

  // Home Dashboard
  "home.welcome": { en: "Welcome back", hi: "पुनः स्वागत है" },
  "home.continueLearning": { en: "Continue Learning", hi: "सीखना जारी रखें" },
  "home.resumeCourse": { en: "Resume Lesson", hi: "पाठ पुनः शुरू करें" },
  "home.todaysGoals": { en: "Today's Learning Goal", hi: "आज का अध्ययन लक्ष्य" },
  "home.learningStreak": { en: "Learning Streak", hi: "अध्ययन निरंतरता" },
  "home.days": { en: "Days Active", hi: "दिन सक्रिय" },
  "home.targetMinutes": { en: "target today", hi: "आज का लक्ष्य" },
  "home.recommended": { en: "Recommended For Your Ministry", hi: "आपके मंत्रालय हेतु अनुशंसित" },
  "home.trending": { en: "Trending Courses", hi: "प्रचलित पाठ्यक्रम" },
  "home.recentlyExplored": { en: "Recently Explored", hi: "हाल ही में देखे गए" },
  "home.futurePlanned": { en: "Future Planned Courses", hi: "आगामी नियोजित पाठ्यक्रम" },
  "home.myProgress": { en: "Learning Progress Snapshot", hi: "प्रगति संक्षिप्त विवरण" },
  "home.competencies": { en: "Acquired Competencies", hi: "अर्जित दक्षताएं" },

  // Discover & Search
  "discover.title": { en: "Course Catalogue & External Training", hi: "पाठ्यक्रम सूची एवं बाह्य प्रशिक्षण" },
  "discover.subtitle": { en: "Empowering Indian Civil Servants with Certified Official Statistical Competencies", hi: "भारतीय सिविल सेवकों को प्रमाणित आधिकारिक सांख्यिकी दक्षताओं से सशक्त बनाना" },
  "discover.searchPlaceholder": { en: "Search by course title, methodology, or ministry...", hi: "शीर्षक, पद्धति या मंत्रालय द्वारा खोजें..." },
  "discover.all": { en: "All Disciplines", hi: "सभी विषय" },
  "discover.popular": { en: "Popular", hi: "लोकप्रिय" },
  "discover.new": { en: "New Releases", hi: "नए संस्करण" },
  "discover.internalOnly": { en: "Internal Karmayogi", hi: "आंतरिक कर्मयोगी" },
  "discover.externalOnly": { en: "External Accredited (ISTM/DoPT)", hi: "बाह्य मान्यता प्राप्त (आईएसटीएम/डीओपीटी)" },
  "discover.source": { en: "Provider Source", hi: "प्रदाता स्रोत" },
  "discover.difficulty": { en: "Difficulty Level", hi: "कठिनाई स्तर" },

  // Course Page
  "course.enrollNow": { en: "Enroll in Course", hi: "पाठ्यक्रम में प्रवेश लें" },
  "course.startLearning": { en: "Start Learning", hi: "सीखना शुरू करें" },
  "course.continue": { en: "Continue Learning", hi: "अध्ययन जारी रखें" },
  "course.syllabus": { en: "Course Syllabus & Curriculum", hi: "पाठ्यक्रम रूपरेखा एवं विषय-सूची" },
  "course.skillsGained": { en: "Competencies Acquired", hi: "अर्जित क्षमताएं" },
  "course.instructor": { en: "Faculty / Instructor", hi: "संकाय / प्रशिक्षक" },
  "course.organization": { en: "Accredited Body", hi: "मान्यता प्राप्त संस्था" },
  "course.duration": { en: "Estimated Duration", hi: "अनुमानित अवधि" },

  // Learning Player
  "learn.markCompleted": { en: "Mark Completed & Next", hi: "पूर्ण चिह्नित करें और आगे बढ़ें" },
  "learn.previous": { en: "Previous Lesson", hi: "पिछला पाठ" },
  "learn.next": { en: "Next Lesson", hi: "अगला पाठ" },
  "learn.practice": { en: "In-Lesson Concept Activity", hi: "पाठ-अंतर्गत संकल्पना अभ्यास" },
  "learn.checkAnswer": { en: "Validate Concept", hi: "उत्तर की पुष्टि करें" },
  "learn.takeAssessment": { en: "Proceed to Final Assessment", hi: "अंतिम मूल्यांकन की ओर बढ़ें" },

  // Assessments
  "assess.instructions": { en: "Assessment Instructions", hi: "मूल्यांकन निर्देश" },
  "assess.passRequirement": { en: "Passing Standard", hi: "उत्तीर्ण मानक" },
  "assess.timeLimit": { en: "Time Allotted", hi: "आवंटित समय" },
  "assess.startAssessment": { en: "Begin Official Assessment", hi: "आधिकारिक मूल्यांकन प्रारंभ करें" },
  "assess.submit": { en: "Submit Examination", hi: "परीक्षा जमा करें" },
  "assess.congratulations": { en: "Assessment Passed!", hi: "मूल्यांकन उत्तीर्ण!" },
  "assess.tryAgain": { en: "Passing Score Not Met", hi: "उत्तीर्ण अंक प्राप्त नहीं हुए" },
  "assess.viewCertificate": { en: "View Official Certificate", hi: "आधिकारिक प्रमाण पत्र देखें" },
  "assess.retake": { en: "Retake Assessment", hi: "पुनः परीक्षा दें" },

  // Certificates & Progress
  "cert.title": { en: "Certificate of Competency", hi: "दक्षता प्रमाण पत्र" },
  "cert.verified": { en: "Official Government Credential Verified", hi: "आधिकारिक सरकारी क्रेडेंशियल सत्यापित" },
  "cert.download": { en: "Print / Save PDF", hi: "प्रिंट / पीडीएफ सुरक्षित करें" },

  // Homepage - Hero
  "hero.title": {
    en: "National Learning Platform for Civil Services",
    hi: "सिविल सेवाओं हेतु राष्ट्रीय शिक्षण मंच",
  },
  "hero.subtitle": {
    en: "Integrated competency frameworks, accredited training modules, and verifiable certifications for India's administrative and statistical officers under Mission Karmayogi.",
    hi: "मिशन कर्मयोगी के अंतर्गत भारत के प्रशासनिक एवं सांख्यिकीय अधिकारियों हेतु एकीकृत क्षमता ढांचा, मान्यता प्राप्त प्रशिक्षण मॉड्यूल एवं सत्यापन योग्य प्रमाणन।",
  },
  "hero.signIn": {
    en: "Official Sign In",
    hi: "आधिकारिक लॉगिन",
  },
  "hero.explore": {
    en: "Explore Catalog",
    hi: "पाठ्यक्रम सूची देखें",
  },
  "hero.badgeMospi": {
    en: "MoSPI Accredited",
    hi: "एमओएसपीआई मान्यता प्राप्त",
  },
  "hero.badgeCbc": {
    en: "CBC Competency Framework",
    hi: "सीबीसी क्षमता ढांचा",
  },
  "hero.badgeIso": {
    en: "ISO/IEC Aligned",
    hi: "आईएसओ/आईईसी मानक",
  },
  "hero.slide1": {
    en: "Mission Karmayogi National Capacity Building",
    hi: "मिशन कर्मयोगी राष्ट्रीय क्षमता निर्माण",
  },
  "hero.slide2": {
    en: "Administrative Cadre Review & Policy Integration",
    hi: "प्रशासनिक संवर्ग समीक्षा एवं नीति समन्वय",
  },
  "hero.slide3": {
    en: "AI-Daksh Official Statistical & Analytical Tools",
    hi: "एआई-दक्ष आधिकारिक सांख्यिकी एवं विश्लेषणात्मक उपकरण",
  },

  // Homepage - Statistics
  "stats.trainedCount": { en: "40,000+", hi: "४०,०००+" },
  "stats.trainedLabel": { en: "Civil Servants Trained", hi: "प्रशिक्षित सिविल सेवक" },
  "stats.trainedSub": { en: "Central ministries & state cadres", hi: "केंद्रीय मंत्रालय एवं राज्य संवर्ग" },
  "stats.modulesCount": { en: "100%", hi: "१००%" },
  "stats.modulesLabel": { en: "Accredited Modules", hi: "मान्यता प्राप्त मॉड्यूल" },
  "stats.modulesSub": { en: "CBC certified curriculum standards", hi: "सीबीसी प्रमाणित पाठ्यक्रम मानक" },
  "stats.qualityCount": { en: "UN-NQAF", hi: "यूएन-एनक्यूएएफ" },
  "stats.qualityLabel": { en: "Quality Assurance", hi: "गुणवत्ता आश्वासन" },
  "stats.qualitySub": { en: "United Nations statistical rubrics", hi: "संयुक्त राष्ट्र सांख्यिकी मानक" },
  "stats.certCount": { en: "Verifiable", hi: "सत्यापन योग्य" },
  "stats.certLabel": { en: "Digital Credentials", hi: "डिजिटल क्रेडेंशियल" },
  "stats.certSub": { en: "Tamper-proof certificate hashes", hi: "छेड़छाड़-मुक्त प्रमाणपत्र डिजिटल हैश" },

  // Homepage - About
  "about.cardOrg": { en: "Mission Karmayogi (MoSPI)", hi: "मिशन कर्मयोगी (एमओएसपीआई)" },
  "about.cardSub": { en: "Capacity Building Commission", hi: "क्षमता निर्माण आयोग" },
  "about.item1Title": { en: "Official Statistical Cadre", hi: "आधिकारिक सांख्यिकी संवर्ग" },
  "about.item1Desc": { en: "Standardized NSS sample surveys, CPI price indices, and National Accounts compilation.", hi: "मानकीकृत एनएसएस नमूना सर्वेक्षण, सीपीआई मूल्य सूचकांक एवं राष्ट्रीय लेखा संकलन।" },
  "about.item2Title": { en: "Accredited 70% Threshold", hi: "मान्यता प्राप्त ७०% उत्तीर्ण सीमा" },
  "about.item2Desc": { en: "Verified assessments awarding official digital credentials recognized in service records.", hi: "सत्यापित मूल्यांकन जो सेवा अभिलेखों में मान्य आधिकारिक डिजिटल क्रेडेंशियल प्रदान करते हैं।" },
  "about.item3Title": { en: "Cadre Intelligence & AI", hi: "संवर्ग आसूचना एवं एआई" },
  "about.item3Desc": { en: "Automated guidance on departmental circulars, survey protocols, and field definitions.", hi: "विभागीय परिपत्रों, सर्वेक्षण प्रोटोकॉल और क्षेत्रीय परिभाषाओं पर त्वरित स्वचालित मार्गदर्शन।" },
  "about.title": { en: "A Competency-Driven Learning Paradigm", hi: "क्षमता-आधारित शिक्षण प्रतिमान" },
  "about.desc": { en: "Transitioning India's civil service from traditional procedural rules to dynamic, role-based competency mastery—aligned with the National Programme for Civil Services Capacity Building (NPCSCB).", hi: "भारतीय सिविल सेवा को पारंपरिक प्रक्रियात्मक नियमों से गतिशील, भूमिका-आधारित क्षमता दक्षता की ओर अग्रसर करना—राष्ट्रीय सिविल सेवा क्षमता निर्माण कार्यक्रम (एनपीसीएससीबी) के अनुरूप।" },
  "about.pillar1Title": { en: "Statistical Integrity & Methodologies", hi: "सांख्यिकीय सत्यनिष्ठा एवं कार्यप्रणाली" },
  "about.pillar1Desc": { en: "Curricula on National Sample Surveys (NSS), Consumer Price Index (CPI), IIP, and National Accounts compilation routines.", hi: "राष्ट्रीय नमूना सर्वेक्षण (एनएसएस), उपभोक्ता मूल्य सूचकांक (सीपीआई), आईआईपी और राष्ट्रीय लेखा संकलन विधियों पर विस्तृत पाठ्यक्रम।" },
  "about.pillar2Title": { en: "Certified Standardized Assessments", hi: "प्रमाणित मानकीकृत मूल्यांकन" },
  "about.pillar2Desc": { en: "Evaluations with a strict 70% passing threshold, awarding verifiable digital credentials linked to personnel service records.", hi: "कड़े ७०% उत्तीर्ण मानक वाले मूल्यांकन, जो कार्मिक सेवा अभिलेखों से जुड़े सत्यापन योग्य डिजिटल क्रेडेंशियल प्रदान करते हैं।" },
  "about.pillar3Title": { en: "AI-Orchestrated Cadre Assistant", hi: "एआई-संचालित संवर्ग सहायक" },
  "about.pillar3Desc": { en: "Built-in civil service assistant offering immediate guidance on survey methodologies, regulatory circulars, and course queries.", hi: "सर्वेक्षण कार्यप्रणाली, विनियामक परिपत्रों एवं पाठ्यक्रम प्रश्नों पर तत्काल मार्गदर्शन प्रदान करने वाला इन-बिल्ट सिविल सेवा सहायक।" },

  // Homepage - How It Works
  "howItWorks.title": { en: "How the Karmayogi Journey Works", hi: "कर्मयोगी शिक्षण यात्रा कैसे कार्य करती है" },
  "howItWorks.subtitle": { en: "A structured four-step path from cadre onboarding to recognized national civil service certification.", hi: "संवर्ग ऑनबोर्डिंग से लेकर मान्यता प्राप्त राष्ट्रीय सिविल सेवा प्रमाणन तक एक संरचित चार-चरणीय मार्ग।" },
  "howItWorks.step1Title": { en: "Onboard Role", hi: "भूमिका ऑनबोर्डिंग" },
  "howItWorks.step1Desc": { en: "Authenticate with official government email and specify your ministry and cadre domain.", hi: "आधिकारिक सरकारी ईमेल से प्रमाणीकरण करें और अपने मंत्रालय तथा संवर्ग कार्यक्षेत्र का चयन करें।" },
  "howItWorks.step2Title": { en: "Discover & Study", hi: "खोजें एवं अध्ययन करें" },
  "howItWorks.step2Desc": { en: "Study accredited video modules, CAPI survey simulations, and field methodology handbooks.", hi: "मान्यता प्राप्त वीडियो मॉड्यूल, सीएपीआई सर्वेक्षण सिमुलेशन और क्षेत्रीय कार्यप्रणाली पुस्तिकाओं का अध्ययन करें।" },
  "howItWorks.step3Title": { en: "Pass Assessment", hi: "मूल्यांकन उत्तीर्ण करें" },
  "howItWorks.step3Desc": { en: "Complete 70% threshold examinations with automated scoring and detailed question reviews.", hi: "स्वचालित मूल्यांकन और विस्तृत प्रश्न समीक्षा के साथ ७०% उत्तीर्ण सीमा वाली परीक्षाएं पूर्ण करें।" },
  "howItWorks.step4Title": { en: "Earn Certificate", hi: "प्रमाणपत्र प्राप्त करें" },
  "howItWorks.step4Desc": { en: "Receive cryptographically verifiable credentials linked to your official civil service record.", hi: "अपने आधिकारिक सिविल सेवा रिकॉर्ड से जुड़े क्रिप्टोग्राफिक रूप से सत्यापन योग्य क्रेडेंशियल प्राप्त करें।" },

  // Homepage - Resources
  "resources.title": { en: "Cadre Resources & Statistical Library", hi: "संवर्ग संसाधन एवं सांख्यिकी पुस्तकालय" },
  "resources.subtitle": { en: "Official survey manuals, quality frameworks, and technical reference handbooks curated by MoSPI, CSO, and NSSO.", hi: "सांख्यिकी मंत्रालय (MoSPI), सीएसओ और एनएसएसओ द्वारा तैयार आधिकारिक सर्वेक्षण नियमावलियां, गुणवत्ता रूपरेखाएं एवं संदर्भ पुस्तिकाएं।" },
  "resources.browseCatalog": { en: "Browse Full Catalog", hi: "संपूर्ण सूची देखें" },
  "resources.access": { en: "Access", hi: "देखें" },
  "resources.doc1Tag": { en: "NSSO Guide", hi: "एनएसएसओ मार्गदर्शिका" },
  "resources.doc1Title": { en: "Field Enumerator Manual", hi: "क्षेत्रीय प्रगणक नियमावली" },
  "resources.doc1Desc": { en: "Concepts, household sampling frameworks, and standardized definitions for socio-economic survey rounds.", hi: "सामाजिक-आर्थिक सर्वेक्षण दौर हेतु संकल्पनाएं, घरेलू नमूना चयन ढांचा और मानकीकृत परिभाषाएं।" },
  "resources.doc2Tag": { en: "Price Statistics", hi: "मूल्य सांख्यिकी" },
  "resources.doc2Title": { en: "CPI & IIP Technical Manual", hi: "सीपीआई एवं आईआईपी तकनीकी नियमावली" },
  "resources.doc2Desc": { en: "Retail price collection routines, item basket weighting diagrams, and index compilation methodologies.", hi: "खुदरा मूल्य संग्रह विधियां, वस्तु टोकरी भार आरेख और सूचकांक संकलन कार्यप्रणाली।" },
  "resources.doc3Tag": { en: "Quality Standards", hi: "गुणवत्ता मानक" },
  "resources.doc3Title": { en: "UN-NQAF Quality Rubrics", hi: "यूएन-एनक्यूएएफ गुणवत्ता रूपरेखा" },
  "resources.doc3Desc": { en: "United Nations National Quality Assurance Framework guidelines adapted for Indian official statistics.", hi: "भारतीय आधिकारिक सांख्यिकी हेतु अनुकूलित संयुक्त राष्ट्र राष्ट्रीय गुणवत्ता आश्वासन ढांचा दिशानिर्देश।" },
  "resources.doc4Tag": { en: "Survey Tech", hi: "सर्वेक्षण तकनीक" },
  "resources.doc4Title": { en: "CAPI Operations Manual", hi: "सीएपीआई संचालन नियमावली" },
  "resources.doc4Desc": { en: "Tablet-based interview setup, encrypted geo-tag synchronization, and automated logic validation procedures.", hi: "टैबलेट-आधारित साक्षात्कार सेटअप, एन्क्रिप्टेड भू-टैग सिंक्रनाइज़ेशन और स्वचालित सत्यापन प्रक्रियाएं।" },

  // Homepage - Help & Support
  "help.title": { en: "Help & Official Training Support", hi: "सहायता एवं आधिकारिक प्रशिक्षण केंद्र" },
  "help.subtitle": { en: "Official support channels for central civil servants, state statisticians, and ministry nodal officers.", hi: "केंद्रीय सिविल सेवकों, राज्य सांख्यिकीविदों और मंत्रालय के नोडल अधिकारियों हेतु आधिकारिक सहायता चैनल।" },
  "help.aiTitle": { en: "24/7 Civil Service AI Assistant", hi: "२४/७ सिविल सेवा एआई सहायक" },
  "help.aiDesc": { en: "Immediate, cited answers from official training manuals, survey sampling protocols, and circular guidelines.", hi: "आधिकारिक प्रशिक्षण नियमावलियों, सर्वेक्षण प्रोटोकॉल और परिपत्रों से तत्काल प्रामाणिक उत्तर प्राप्त करें।" },
  "help.aiLaunch": { en: "Launch AI Assistant", hi: "एआई सहायक प्रारंभ करें" },
  "help.deskTitle": { en: "Ministry Training Desk", hi: "मंत्रालय प्रशिक्षण सहायता केंद्र" },
  "help.deskDesc": { en: "For cadre verification, department approvals, or official nomination queries, reach out to the Central Training Division.", hi: "संवर्ग सत्यापन, विभागीय अनुमोदन या आधिकारिक नामांकन हेतु केंद्रीय प्रशिक्षण प्रभाग से संपर्क करें।" },
  "help.hours": { en: "Mon – Fri, 09:30 – 18:00 IST", hi: "सोम – शुक्र, ०९:३० – १८:०० आईएसटी" },
  "help.faqTitle": { en: "Frequently Asked Questions", hi: "अक्सर पूछे जाने वाले प्रश्न" },
  "help.faq1Q": { en: "How do I verify certificates?", hi: "प्रमाणपत्रों का सत्यापन कैसे करें?" },
  "help.faq1A": { en: "Every certificate includes a verifiable SHA-256 hash at /certificates.", hi: "प्रत्येक प्रमाणपत्र में /certificates पर सत्यापित करने योग्य एक SHA-256 हैश शामिल होता है।" },
  "help.faq2Q": { en: "What is the module pass threshold?", hi: "मॉड्यूल उत्तीर्ण करने की न्यूनतम सीमा क्या है?" },
  "help.faq2A": { en: "MoSPI accredited certifications require a 70% passing score on final evaluations.", hi: "एमओएसपीआई मान्यता प्राप्त प्रमाणन हेतु अंतिम मूल्यांकन में ७०% अंक आवश्यक हैं।" },
  "help.knowledgeBase": { en: "Knowledge Base", hi: "ज्ञान कोष" },

  // Homepage - Closing Banner
  "cta.readyTitle": { en: "Ready to advance your official competencies?", hi: "अपनी आधिकारिक क्षमताओं को सशक्त बनाने के लिए तैयार हैं?" },
  "cta.readyDesc": { en: "Sign in with your official government credentials or register with your nodal department officer today.", hi: "अपने आधिकारिक सरकारी क्रेडेंशियल से साइन इन करें या आज ही अपने नोडल विभाग अधिकारी से संपर्क कर पंजीकरण करें।" },
  "cta.register": { en: "Register New Official", hi: "नया अधिकारी पंजीकरण" },
  "cta.copyright": { en: "© 2026 iGOT Karmayogi Bharat • Capacity Building Commission • Ministry of Statistics & Programme Implementation", hi: "© २०२६ आईगॉट कर्मयोगी भारत • क्षमता निर्माण आयोग • सांख्यिकी एवं कार्यक्रम कार्यान्वयन मंत्रालय" },
  "cta.privacy": { en: "Privacy Policy", hi: "गोपनीयता नीति" },
  "cta.terms": { en: "Terms of Service", hi: "सेवा की शर्तें" },
  "cta.dataGov": { en: "Data Governance", hi: "डेटा प्रशासन" },
  "cta.helpdesk": { en: "Helpdesk", hi: "सहायता केंद्र" }
};

interface I18nContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const I18nContext = createContext<I18nContextType>({
  language: "en",
  setLanguage: () => {},
  t: (key: string) => key,
});

export function I18nProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Language>("en");

  useEffect(() => {
    const saved = localStorage.getItem("karmayogi_lang") as Language;
    if (saved && (saved === "en" || saved === "hi")) {
      setLanguageState(saved);
    }
  }, []);

  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    localStorage.setItem("karmayogi_lang", lang);
  };

  const t = (key: string): string => {
    const entry = translations[key];
    if (!entry) return key;
    return entry[language] || entry.en || key;
  };

  return (
    <I18nContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  return useContext(I18nContext);
}
