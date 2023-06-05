function fetchScoreData() {
    fetch('http://localhost:8880/ScoreData.json')
    .then(response => {
      console.log(response.status)
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Failed to fetch data');
      }
    })
    .then(data => {
      let empDetailsScores = data.emp_details;
      let boxElement = document.querySelector('#box');
  
      boxElement.innerHTML = "";
      empDetailsScores.forEach(score => {
        let h3Element = document.createElement('h3');
        h3Element.innerHTML = score;  
        h3Element.style.fontSize = '20px';
        h3Element.style.color = 'green';
        boxElement.appendChild(h3Element);
      });
      fetchScoreData();
    })
    .catch(error => {
      console.error('Error:', error);
      fetchScoreData();
    });
  }
  
  
  fetchScoreData();
  
  