document.getElementById('searchForm').onsubmit = function(event) {
  event.preventDefault();
  
  var text = document.getElementById('text').value;
  var area = document.getElementById('area').value;
  var only_with_salary = document.getElementById('only_with_salary').checked;
  var per_page = document.getElementById('per_page').value;
  var page = document.getElementById('page').value;

  const data = {
    text: text,
    area: parseInt(area),
    only_with_salary: only_with_salary,
    per_page: parseInt(per_page),
    page: parseInt(page)
  };

  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:80/api/hh/vacancies', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function() {
      if (xhr.readyState == 4 && xhr.status == 200) {
          var response = JSON.parse(xhr.responseText);
          displayResults(response);
      }
  };
  xhr.send(JSON.stringify(data));
};

function displayResults(data) {
  var results = document.getElementById('results');
  results.innerHTML = '';

  data.items.forEach(function(item) {
      var card = document.createElement('div');
      card.className = 'vacancy-card';

      var title = document.createElement('h2');
      title.textContent = item.name;
      card.appendChild(title);

      var salary = document.createElement('p');
      salary.textContent = 'Зарплата: ' + (item.salary && item.salary.from ? 'от ' + item.salary.from : '') + 
                           (item.salary && item.salary.to ? ' до ' + item.salary.to : '') + 
                           ' ' + (item.salary ? item.salary.currency : '');
      card.appendChild(salary);

      var employer = document.createElement('p');
      employer.textContent = 'Работодатель: ' + (item.employer ? item.employer.name : '');
      card.appendChild(employer);

      var description = document.createElement('p');
      description.textContent = 'Описание: ' + (item.snippet ? item.snippet.requirement : '');
      card.appendChild(description);

      var applyLink = document.createElement('a');
      applyLink.href = item.apply_alternate_url;
      applyLink.textContent = 'Откликнуться';
      applyLink.target = '_blank';
      card.appendChild(applyLink);

      results.appendChild(card);
  });
}
