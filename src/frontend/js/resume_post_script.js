document.getElementById('searchForm').addEventListener('submit', function(event) {
  event.preventDefault();
  
  const searchText = document.getElementById('text').value;
  const currency = document.getElementById('currency').value;
  const salaryFrom = document.getElementById('salaryFrom').value;
  const salaryTo = document.getElementById('salaryTo').value;
  const area = document.getElementById('area').value;
  const label = document.getElementById('label').value;
  const age_from = document.getElementById('age_from').value;
  const age_to = document.getElementById('age_to').value;
  const page = document.getElementById('page').value;
  const per_page = document.getElementById('per_page').value;

  const data = {
      text: searchText,
      currency: currency,
      salary_from: parseInt(salaryFrom),
      salary_to: parseInt(salaryTo),
      area : parseInt(area),
      label : label,
      age_from : parseInt(age_from),
      age_to : parseInt(age_to),
      page : parseInt(page),
      per_page : parseInt(per_page),
  };

var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:80/api/hh/resumes', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function() {
      if (xhr.readyState == 4 && xhr.status == 200) {
          var response = JSON.parse(xhr.responseText);
          displayResults(response);
      }
  };
  xhr.send(JSON.stringify(data));

function displayResults(data) {
  var results = document.getElementById('results');
  results.innerHTML = '';

  var found = document.createElement('h1');
  found.textContent = data.found;
  results.appendChild(found);

  data.items.forEach(function(item) {
    var card = document.createElement('div');
    card.className = 'vacancy-card';


    var text = document.createElement('h2');
    text.textContent = item.text;
    card.appendChild(text);

    var area = document.createElement('p');
    area.textContent = 'Область: ' + (item.area);
    card.appendChild(area);

    var age = document.createElement('p');
    age.textContent = 'Возраст: ' + (item.age);
    card.appendChild(age);

    var salary = document.createElement('p');
    salary.textContent = 'Зарплата: ' + (item.salary);
    card.appendChild(salary);

    var experience = document.createElement('p');
    experience.textContent = 'Опыт: ' + (item.experience);
    card.appendChild(experience);

    var applyLink = document.createElement('a');
    applyLink.href = item.link;
    applyLink.textContent = 'Просмотреть резюме';
    applyLink.target = '_blank';
    card.appendChild(applyLink);

    results.appendChild(card);
  });
}});