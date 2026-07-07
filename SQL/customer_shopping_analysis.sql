SELECT * 
FROM shopping_trends_updated;

SELECT COUNT(*) AS Total_Customers
FROM shopping_trends_updated;

SELECT AVG(Age) AS Average_Age
FROM shopping_trends_updated;

SELECT Gender,
COUNT(*) AS Total_Customers
FROM shopping_trends_updated
GROUP BY Gender;

SELECT Category,
SUM(Purchase_Amount_USD) AS Total_Sales
FROM shopping_trends_updated
GROUP BY Category
ORDER BY Total_Sales DESC;

SELECT AVG(Purchase_Amount_USD) AS Average_Purchase
FROM shopping_trends_updated;

SELECT MAX(Purchase_Amount_USD) AS Highest_Purchase
FROM shopping_trends_updated;

SELECT MIN(Purchase_Amount_USD) AS Lowest_Purchase
FROM shopping_trends_updated;

SELECT Gender,
SUM(Purchase_Amount_USD) AS Total_Sales
FROM shopping_trends_updated
GROUP BY Gender;

SELECT Season,
SUM(Purchase_Amount_USD) AS Total_Sales
FROM shopping_trends_updated
GROUP BY Season
ORDER BY Total_Sales DESC;

SELECT TOP 10 *
FROM shopping_trends_updated
ORDER BY Purchase_Amount_USD DESC;

SELECT Subscription_Status,
COUNT(*) AS Customers
FROM shopping_trends_updated
GROUP BY Subscription_Status;

SELECT Payment_Method,
COUNT(*) AS Total
FROM shopping_trends_updated
GROUP BY Payment_Method
ORDER BY Total DESC;

SELECT Category,
AVG(Review_Rating) AS Average_Rating
FROM shopping_trends_updated
GROUP BY Category
ORDER BY Average_Rating DESC;

SELECT Location,
SUM(Purchase_Amount_USD) AS Total_Sales
FROM shopping_trends_updated
GROUP BY Location
ORDER BY Total_Sales DESC;

SELECT Category,
SUM(Purchase_Amount_USD) AS Total_Sales
FROM shopping_trends_updated
GROUP BY Category
HAVING SUM(Purchase_Amount_USD) > 10000;

SELECT Gender,
AVG(Purchase_Amount_USD) AS Average_Purchase
FROM shopping_trends_updated
GROUP BY Gender;

SELECT *
FROM shopping_trends_updated
WHERE Age > 50;

SELECT *
FROM shopping_trends_updated
WHERE Review_Rating > 4.5;

SELECT
CASE
    WHEN Age < 20 THEN 'Teen'
    WHEN Age BETWEEN 20 AND 39 THEN 'Young Adult'
    WHEN Age BETWEEN 40 AND 59 THEN 'Adult'
    ELSE 'Senior'
END AS Age_Group,
COUNT(*) AS Customers
FROM shopping_trends_updated
GROUP BY
CASE
    WHEN Age < 20 THEN 'Teen'
    WHEN Age BETWEEN 20 AND 39 THEN 'Young Adult'
    WHEN Age BETWEEN 40 AND 59 THEN 'Adult'
    ELSE 'Senior'
END
ORDER BY Customers DESC;

