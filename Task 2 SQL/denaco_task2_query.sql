
WITH RegionSales AS (
    SELECT 
        Region,
        SUM(Sales) AS total_region_sales
    FROM Sales
    GROUP BY Region
),
AboveAvgRegions AS (
    SELECT 
        Region
    FROM RegionSales
    WHERE total_region_sales > (
        SELECT AVG(total_region_sales) FROM RegionSales
    )
)
SELECT 
    s.Region,
    s.Category,
    SUM(s.Sales) AS Total_Revenue
FROM Sales s
JOIN AboveAvgRegions r
    ON s.Region = r.Region
GROUP BY s.Region, s.Category
ORDER BY s.Region, s.Category;
