CREATE TABLE classes (
  id INTEGER PRIMARY KEY,
  day TEXT NOT NULL,
  week TEXT NOT NULL,
  position INTEGER NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  course TEXT NOT NULL,
  course_type TEXT NOT NULL,
  instructor TEXT NOT NULL,
  location TEXT NOT NULL
);

INSERT INTO classes (day, week, position, start_time, end_time, course, course_type, instructor, location)
VALUES ('Monday', 'even', 1, '10:50', '12:25', 'Физика', 'Лекционные', 'Блохин Д. И.', 'Б-3'),
('Tuesday', 'even', 2, '12:40', '14:15', 'Иностранный язык', 'Практические', 'Не указан', 'Каф. ИЯКТ'),
('Wednesday', 'even', 1, '09:00', '10:35', 'Физическая культура и спорт', 'Практические', 'Преподаватель не указан', 'Каф. ФКИЗ'),
('Friday', 'even', 2, '10:50', '12:25', 'Математика', 'Лекционные', 'Плужникова Е. Л.', 'Б-3');

INSERT INTO classes (day, week, position, start_time, end_time, course, course_type, instructor, location) 
VALUES ('Friday', 'odd', 1, '09:00', '10:35', 'Основы дискретной математики', 'Практические', 'Кружкова Г. В.', 'А-509'),
('Monday', 'odd', 2, '10:50', '12:25', 'Физика', 'Лекционные', 'Блохин Д. И.', 'Б-3'),
('Thursday', 'odd', 3, '12:40', '14:15', 'Иностранный язык', 'Не указан', 'Каф. ИЯКТ'),
('Wednesday', 'odd', 4, '14:30', '16:05', 'Персональная эффективность', 'Практические', 'Мотора Л. С.', 'А-304');