document.getElementById('searchForm').addEventListener('submit', function(event) {
  event.preventDefault();
  
  const searchText = document.getElementById('searchText').value;
  const currency = document.getElementById('currency').value;
  const salaryFrom = document.getElementById('salaryFrom').value;
  const salaryTo = document.getElementById('salaryTo').value;
  const area = document.getElementById('area');
  const label = document.getElementById('label');
  const age_from = document.getElementById('age_from');
  const age_to = document.getElementById('age_to');
  const relocation = document.getElementById('relocation');
  const period = document.getElementById('period');
  const education_level = document.getElementById('education_level');
  const employment = document.getElementById('employment');
  const skill = document.getElementById('skill');
  const gender = document.getElementById('gender');
  const language = document.getElementById('language');
  const schedule = document.getElementById('schedule');
  const order_by = document.getElementById('order_by');
  const citizenship = document.getElementById('citizenship');
  const work_ticket = document.getElementById('work_ticket');
  const page = document.getElementById('page');
  const per_page = document.getElementById('per_page');

  const data = {
      text: searchText,
      currency: currency,
      salary_from: salaryFrom,
      salary_to: salaryTo,
      area : area,
      label : label,
      age_from : age_from,
      age_to : age_to,
      relocation : relocation,
      period : period,
      education_level : education_level,
      employment : employment,
      skill : skill,
      gender : gender,
      language : language,
      schedule : schedule,
      order_by : order_by,
      citizenship : citizenship,
      work_ticket : work_ticket,
      page : page,
      per_page : per_page,
  };

  fetch('http://localhost:8000/api/hh/resumes', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
      const resultsElement = document.getElementById('results');
      resultsElement.innerHTML = ''; // Очистить предыдущие результаты
      data.items.forEach(item => {
          const div = document.createElement('div');
          div.innerHTML = `Резюме: ${item.text} - ЗП: ${item.salary}`;
          resultsElement.appendChild(div);
      });
  })
  .catch(error => console.error('Ошибка:', error));
});
