import bennyIcon from './assets/benny_icon.png';

/* Mock data for the daily checkin */
export const checkinFlow = [
  {
    type: 'ai',
    text: "Hi Jimmy! Ready for our daily check-in? Let's start with your nutrition. How did you feel about your food choices today?",
    buttons: ['Feeling Great', 'It was Okay', 'Needs Improvement'],
    icon: bennyIcon,
  },
  {
    type: 'ai',
    text: "That's fantastic! Now for fitness. Did you complete your planned activity today?",
    buttons: ['Yes', 'No'],
    icon: bennyIcon,
  },
  {
    type: 'ai',
    text: 'Awesome work! Finally, let\'s check in on your well-being. How would you rate your stress levels today?',
    buttons: ['Low', 'Medium', 'High'],
    icon: bennyIcon,
  },
  {
    type: 'ai',
    text: 'Thanks for completing your check-in. You\'re doing great!',
    buttons: [], // End of check-in
    icon: bennyIcon,
  },
];