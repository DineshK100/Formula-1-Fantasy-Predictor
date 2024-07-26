# Formula 1 Fantasy Predictor

## A fully functional Formula 1 optimal fantasy team selector as well as podium/grid finishes project that is coded in Python backend and a React.js frontend.

### Backend

I developed the backend scripts through the use of Python with the server running on Flask.

- Web Scraping: I found a database online (https://pitwall.app/) that stored all the necessary race data that I had needed. I then used the BeautifulSoup4 Python Library to scrape race data from 1990 - 2024, which would later be used to train my machine learning model.

- Server: The Flask framework was chosen for its simplicity and effectiveness in handling web requests in Python. It serves as the backbone of the server, managing API endpoints and ensuring smooth communication between the frontend and backend.
  
- Databases:
  - MongoDB: This NoSQL database is used to store the vast amount of race data scraped from Pitwall. Using the pymongo library, I established connections to MongoDB within my Python scripts, allowing efficient data storage and retrieval.
  - PostgreSQL: For storing user information such as usernames, passwords, and fantasy log data, I opted for PostgreSQL. Flask's sqlalchemy library facilitated the integration, providing a robust and secure relational database solution.

- Machine Learning Models: After extensive research and experimentation, I selected the XGBoost model for its superior performance in handling structured data. Despite the challenges of limited data and the recent addition of some races, the model achieved an accuracy of up to 70% in several race predictions. This was accomplished by training the model on the historical race data and fine-tuning it for better performance.

- Authentication: The application implements JWT (JSON Web Token) based authentication to secure user sessions and ensure that only authenticated users can access certain endpoints. This mechanism provides a secure and scalable way to manage user authentication.

- Password Safety:
  - Hashing Algorithm: User passwords are securely hashed using the pbkdf2:sha256 algorithm through the werkzeug security library before storing them in the database. This algorithm is chosen for its resistance to brute-force attacks, utilizing a key derivation function that applies a pseudorandom function to the input password along with a salt value and repeats the process multiple times to produce a derived key.
  - Secret Key Generation: To enhance security further, I developed a custom Python script to create a unique secret key. This key is used in hashing and salting processes to add an additional layer of protection. The script generates a random string of characters using a combination of letters, digits, and special characters, ensuring a highly secure and unpredictable key.

### Frontend

- React.js: React.js was chosen for its component-based architecture, which facilitates the development of a modular and maintainable user interface. It allows for efficient state management and re-rendering of components, ensuring a seamless user experience.

- Bootstrap: Some of the design elements such as the Signup and Login pages are designed through the use of Bootstrap inline styling.

- CSS: Every single component and webpage for this project was styled through using CSS

![Screenshot 2024-07-26 at 4 57 38 PM](https://github.com/user-attachments/assets/60379fc2-2e83-45b9-a9b8-520840c2c04c)

![image](https://github.com/user-attachments/assets/ce54fb41-fec8-4d8f-8866-410d83610e44)

![image](https://github.com/user-attachments/assets/5d0c909d-6791-45ef-9e77-00b07ba71075)

![image](https://github.com/user-attachments/assets/6bfba48f-6402-4a22-83e7-a3fffbd0c972)

![image](https://github.com/user-attachments/assets/48f3eb89-9535-43a0-a115-1e2dccf4c484)

### Features

- Predictions: This algorithm takes all the race data available for the race the user selected and comes up with an accurate run down of the final places of all the drivers in the current F1 lineups.

- Fantasy: This incorporates a greedy algorithm in which the drivers and constructors are sorted on price per points and are optimally selected to make the most out of the $100 million budget and find you the best fantasy team to score the maximum points for that race weekend
    - I had initially tried to scrape the data of the real-time prices of the drivers from a database but upon further inspection all the databases I was trying to scrape required me to use Selenium and a web-driver, but due to the time contrainst I placed on myself when developing this project I couldn't teach myself these topics and instead chose to keep the predictions based on the starting driver prices for the 2024 season.

- Fantasy Log: I wanted users to be able to have a sort of log so they can track and monitor their progress as they moved along in the season. The data was fetched from my POSTgreSQL server and displayed using Chart.js.
