import dotenv from 'dotenv';
import mysql from 'mysql';

dotenv.config();  // Load the environment variables

export const pool = mysql.createPool({
  connectionLimit: 10,
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME
});
