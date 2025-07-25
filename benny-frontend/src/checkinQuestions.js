import bennyIcon from './assets/benny_icon.png';

export const checkinQuestions = [
    {
      id: 1,
      type: 'ai',
      text: "Hi! Ready for our daily check-in? How did you feel about your nutrition choices today?",
      category: "nutrition",
      buttons: ["Excellent", "Good", "Okay", "Poor"],
      icon: bennyIcon
    },
    {
      id: 2,
      type: 'ai',
      text: "And how would you rate your sleep last night?",
      category: "sleep", 
      buttons: ["Very good", "Good", "Okay", "Poor"],
      icon: bennyIcon
    },
    {
      id: 3,
      type: 'ai',
      text: "Now for fitness. Did you complete your planned fitness activity today?",
      category: "fitness",
      buttons: ["Yes, completed", "Partially completed", "No, skipped"],
      icon: bennyIcon
    },
    {
      id: 4,
      type: 'ai',
      text: "Finally, let's check in on your well-being. How would you rate your stress levels today?",
      category: "stress",
      buttons: ["Low", "Moderate", "High", "Very high"],
      icon: bennyIcon
    },
    {
      id: 5,
      type: 'ai',
      text: "Thanks for completing your check-in! Wait around for Benny's Daily Recommendation.",
      category: "completion",
      buttons: [], // No buttons for completion message
      icon: bennyIcon
    }
  ];

