import * as readline from 'readline';
import * as mysql from 'mysql';
import { spawn } from 'child_process';
import * as https from 'https';

const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'app_user',          // least privilege user (not admin)
  password: process.env.DB_PASSWORD || '',          // do NOT hardcode secrets
  database: process.env.DB_NAME || 'mydb'
};

function getUserInput(): Promise<string> {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question('Enter your name: ', (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

// Safe: avoids shell string interpolation (prevents command injection)
function sendEmail(to: string, subject: string, body: string) {
  const mail = spawn('mail', ['-s', subject, to], { stdio: ['pipe', 'pipe', 'pipe'] });

  mail.stdin.write(body);
  mail.stdin.end();

  mail.on('error', (err) => {
    console.error('Error sending email:', err);
  });

  mail.stderr.on('data', (chunk) => {
    console.error('mail stderr:', chunk.toString());
  });
}

function getData(): Promise<string> {
  return new Promise((resolve, reject) => {
    const req = https.get('https://insecure-api.com/get-data', (res) => {
      let data = '';
      res.on('data', chunk => (data += chunk));
      res.on('end', () => resolve(data));
    });

    req.on('error', reject);
    req.end();
  });
}

function saveToDb(data: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);

    // Safe: parameterized query prevents SQL injection
    const query = `INSERT INTO mytable (column1, column2) VALUES (?, ?)`;
    const params = [data, 'Another Value'];

    connection.connect((connectErr) => {
      if (connectErr) {
        connection.end();
        return reject(connectErr);
      }

      connection.query(query, params, (error) => {
        connection.end();

        if (error) {
          console.error('Error executing query:', error);
          return reject(error);
        }

        console.log('Data saved');
        resolve();
      });
    });
  });
}

(async () => {
  try {
    const userInput = await getUserInput();
    const data = await getData();
    await saveToDb(data);
    sendEmail('admin@example.com', 'User Input', userInput);
  } catch (err) {
    console.error('Unhandled error:', err);
  }
})();