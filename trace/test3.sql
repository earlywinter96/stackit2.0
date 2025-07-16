SELECT
  manager.name AS manager_name,
  COUNT(employee.id) AS report_count,
  FLOOR(AVG(employee.age)) AS average_age
FROM
  employees AS employee
JOIN
  employees AS manager
  ON employee.reports_to = manager.id
WHERE
  employee.reports_to IS NOT NULL
GROUP BY
  manager.name
ORDER BY
  manager.name;
