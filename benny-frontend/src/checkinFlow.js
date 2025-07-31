import bennyIcon from './assets/benny_icon.png';

/* Mock data for the daily checkin */
export const checkinFlow = [
  {
    type: 'ai',
    text: "Hi! I'm Benny, your personal recipe assistant. What type of meal are you looking to create today?",
    buttons: ['Breakfast', 'Lunch', 'Dinner', 'Dessert'],
    icon: bennyIcon,
  },
  {
    type: 'ai',
    text: "Excellent choice! How much time are you working with for this meal?",
    buttons: ['Under 30 min', '30-60 min', 'More than an hour'],
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