document.getElementById('searchForm').onsubmit = function(event) {
  event.preventDefault();
  
  var text = document.getElementById('text').value;
  var area = document.getElementById('area').value;

  if(text && area) {
    var url = `http://localhost:80/api/scraper/hh/vacancies?text=${text}&area=${area}`;
  } if(text) {
    var url = `http://localhost:80/api/scraper/hh/vacancies?text=${text}`;
  } if(area) {
    var url = `http://localhost:80/api/scraper/hh/vacancies?area=${area}`;
  }else {
    var url = 'http://localhost:80/api/scraper/hh/vacancies'
  }

  fetch(url)
    .then(response => {
      if (!response.ok) {
        if (response.status === 401) {
          alert('Пользователь не авторизован!');
          window.location.href = 'http://localhost/pages/login.html'
        } else {
          alert('Произошла ошибка при выполнении запроса. Код ошибки: ' + response.status);
        }
    }
    return response.json();
    })
    .then(data => {
        displayResults(data);
    })
    .catch(error => console.error('Ошибка:', error));
};

function displayResults(data) {
  var results = document.getElementById('results');
  results.innerHTML = '';

  data.forEach(function(item) {
      var card = document.createElement('div');
      card.className = 'vacancy-card';

      var title = document.createElement('h2');
      title.textContent = item.text;
      card.appendChild(title);

      var salary = document.createElement('p');
      salary.textContent = 'Зарплата: ' + (item.salary.from ? 'от ' + item.salary.from : '') + 
                           (item.salary.to ? ' до ' + item.salary.to : '') + 
                           ' ' + item.salary.currency;
      card.appendChild(salary);

      var area = document.createElement('p');
      area.textContent = 'Регион: ' + item.area
      card.appendChild(area) 

      var link = document.createElement('a');
      link.href = item.link;
      link.textContent = 'Подробнее';
      link.target = '_blank';
      card.appendChild(link);

      results.appendChild(card);
  });
};

function handleError(status, responseText) {
  console.error('Ошибка запроса:', status, responseText);
  if (status == 401) {
    alert('Пользователь не авторизован!');
  } else {
    alert('Произошла ошибка при выполнении запроса. Код ошибки: ' + status);
  }
};
