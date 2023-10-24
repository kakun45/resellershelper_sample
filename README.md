# Classy Graphs's sample code
## Author - Xeniya Shoiko, All rights reserved.
My repo for the entire project is private I'm adding these files here for a demo purpose only. This is NOT a complete code.

`Classy Graphs` is a comprehensive Python-based tool designed to streamline and optimize various metrics for resellers in the e-commerce domain. This project primarily targets resellers who deal with multiple marketplaces and need a unified platform to manage their KPIs, track sales, and analyze their performance. I started it in 2020 when Poshmark had no dashboard for sellers, just the .CSV sales report. As a seller, I knew exactly what I needed, and I decided to make it. The dashboard exists in the app as of today, but the metrics are limited.

Here is a sample run of the application https://drive.google.com/drive/folders/1ouAag71SeoWP2P_t0qaxfUevsI5LKmmc?usp=sharing

Users: Poshmark sellers, which are ~50% of 80 mln users, with the potential to expand to Etsy, Merkari, etc. sellers. 

Are you a Poshmark seller, know how to code in Python and build React, and would like to contribute to open source? Please [reach out](mailto:xeniya.shoiko@outlook.com). 

## Key Features:

# Multi-Marketplace Integration: 
`Classy Graph` offers seamless integration with popular e-Commerce platforms like eBay, Poshmark, and Mercari (the sample included is for Poshmark). This enables users to manage their metrics in sales and stocks across multiple platforms from a centralized dashboard.

# Sales Analytics and Reporting: 
`Classy Graphs` provides in-depth analytics on sales performance, from a pro seller's point of view, allowing users to track their revenue, identify best-selling products, seasonality of categories, and assess the effectiveness of their pricing strategies.

## INPUT file fields (data in CSV)
```
Listing Date | Order Date | SKU	Order Id | Listing Title | Department | Category | Subcategory | Brand | Color | Size | Bundle Order? | Offer Order | NWT | Cost Price | Order Price | Seller Shipping Discount | Upgraded Shipping Label Fee | Net Earnings | Buyer State | Buyer Zip Code | Buyer Username | Sales Tax (Paid by Buyer) | Sales Tax (Paid by Seller) | Notes | Other Info		
```
## OUTPUT automated analytic: graphs and dashboard samples (not all of them)
<img width="775" alt="Dashboard" src="https://github.com/kakun45/resellershelper_sample/assets/53381916/0f617dce-b39b-415f-8980-a0a99b27c97d">

I am exploring the top 10 buyer states to gain insights into the consumer base. Understand their location for strategic decision-making. Uncover tax exemptions, holidays, and more. Optimize sourcing, timing, and outreach for maximum impact. For precise insights, consider a customized subscription. The 'Net Earnings' metric is utilized for accurate mapping. If the Upper map highlights 'scratched off' states there are no purchases. Geographical convenience is prioritized for far states and territories. Still working on including 'FM', 'MH', 'PW' territories. The map below delves into Zip Code-level details for each buyer. Points are sized and colored by purchase value. Geographic accuracy is maintained, though some points may appear in the sea due to low resolution. Apologies, Puerto Rico.
<img width="1173" alt="Map by state" src="https://github.com/kakun45/resellershelper_sample/assets/53381916/39ebae35-dabb-443d-af61-c9fdccf3d00f">
![Map by Sz of purchase](https://github.com/kakun45/resellershelper_sample/assets/53381916/e4f733f2-4b73-41b8-9e28-89a9c5fd446c)

Discovering the Best Selling Categories. Optimize Your Closet/Boutique: Barplots effectively display value counts, enabling a thorough analysis of strengths and areas for improvement. This graph tallies individually sold items, even those bundled. It offers a visual breakdown of your best- and least-performing Categories. The accompanying tables feature the Top 5 Categories in both high and low performance. While Category data is reliable, Subcategories may be absent. We're eager to delve deeper into Subcategories for a comprehensive analysis. Customized 'Top-"number"' options are available upon request.

![CategoryCount2020](https://github.com/kakun45/resellershelper_sample/assets/53381916/2de2e670-8938-4998-939f-d5669ed54b25)

Applying unsupervised machine learning, specifically the K-means clustering algorithm, to discover patterns in the data. Brought in my domain knowledge to help interpret the clusters. I visualized clusters along two main axes of interest.

![kmeansCluster0-N](https://github.com/kakun45/resellershelper_sample/assets/53381916/3c7d196a-e061-4aeb-b6ee-112587f12797)

Analyzing seasonality on multiple levels, color-coding, grouping, comparing to showcase the trends.
![scatter plot 3_20](https://github.com/kakun45/resellershelper_sample/assets/53381916/6a7c25ae-d602-4d9b-9a83-c5035b222e90)

Advising. Master Your Spending Tracking: 65% of Americans are unsure about last month's expenses. Uncover Posh's 20% fee intricacies and navigate red tape barriers. Consider $15 base price, shipping and bundle discounts, and additional costs. Tailor your pricing strategy for optimal results. Even for potential negative earnings scenarios (e.g., for tax purposes), understanding your limits is invaluable. The graph showcases two color-coded scenarios: 20% fee and beyond. Explore reasons for 25%, 30%, and occasionally 70% fees, from base price to discounts. Customizable bundle options available. Account for COGS, expenses, and taxes for true earnings insight.

![sr_total_fees_paid](https://github.com/kakun45/resellershelper_sample/assets/53381916/580ae22d-23ae-4950-a4f6-81d44a29b368)
