const createPrescriptionTable = `
CREATE TABLE IF NOT EXISTS prescriptions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  doctor_id INT,
  title VARCHAR(255),
  description TEXT,
  file_url TEXT NOT NULL,
  issued_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
`;


export default createPrescriptionTable