document.getElementById('searchForm').onsubmit = function(event) {
  event.preventDefault();
  
  var text = document.getElementById('text').value;
  var area = document.getElementById('area').value;


  if(text && area) {
    var url = `http://localhost:80/api/hh/resumes?text=${text}&area=${area}`;
  } if(text) {
    var url = `http://localhost:80/api/hh/resumes?text=${text}`;
  } if(area) {
    var url = `http://localhost:80/api/hh/resumes?area=${area}`;
  }else {
    var url = 'http://localhost:80/api/hh/resumes'
  }

  fetch(url)
    .then(response => response.json())
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
}
