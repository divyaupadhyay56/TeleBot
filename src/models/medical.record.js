const createMedicalRecordTable = `
CREATE TABLE IF NOT EXISTS medical_records (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  record_type ENUM('visit', 'diagnosis', 'lab', 'prescription') NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  record_date DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
`;

export default createMedicalRecordTable;
