function getNextWorkingDay(date) {
    const dayOfWeek = date.getDay();
    
    if (dayOfWeek === 5) { // Friday
      date.setDate(date.getDate() + 3); // Move to Monday
    } else if (dayOfWeek === 6) { // Saturday
      date.setDate(date.getDate() + 2); // Move to Monday
    } else {
      date.setDate(date.getDate() + 1); // Move to next day
    }
  
    return date;
  }
  
  const inputDates = document.querySelectorAll('#inputDate');
  const today = new Date();
  const nextWorkingDay = getNextWorkingDay(today);
  
  // Format the next working day as "YYYY-MM-DD"
  const formattedDate = nextWorkingDay.toISOString().split('T')[0];
  
  inputDates.forEach(input => {
      input.value = formattedDate;
  });
  