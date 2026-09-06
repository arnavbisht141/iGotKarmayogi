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
  "nav.askAi": { en: "Karmayogi AI", hi: "कर्मयोगी एआई" },

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
  "cert.download": { en: "Print / Save PDF", hi: "प्रिंट / पीडीएफ सुरक्षित करें" }
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
