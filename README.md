# Classy Graphs's sample code
## Author - Xeniya Shoiko, All rights reserved.
**Note:** My repository for the entire project is private. I'm including these files here for demo purposes only. This is **not** the complete code.

## Classy Graphs
Classy Graphs is a comprehensive Python-based tool designed to streamline and optimize key performance metrics for resellers in the e-commerce space. It primarily serves resellers operating across multiple marketplaces who need a unified platform to manage KPIs, track sales, and analyze performance.

I started building this in 2020, back when Poshmark didn’t offer sellers a dashboard—only a .CSV sales report. As a seller myself, I knew exactly what was missing and decided to build the tool I needed. While Poshmark has since added a basic dashboard, the metrics remain limited.

Here is a sample run of the application https://drive.google.com/drive/folders/1ouAag71SeoWP2P_t0qaxfUevsI5LKmmc?usp=sharing

## Target Users

Poshmark sellers (the platform reports having over 8 million sellers) with potential expansion to Etsy, Mercari, and other marketplaces.

Are you a Poshmark seller with Python and React skills interested in contributing to open source? Or interested in testing it? Please, reach out. [reach out](mailto:xeniya.shoiko@outlook.com). 

# Key Features:

## Multi-Marketplace Integration 
Classy Graphs integrates with popular platforms like eBay, Poshmark, and Mercari (sample provided focuses on Poshmark), allowing users to manage sales and inventory metrics from a single dashboard.

## Sales Analytics and Ad-hoc Reporting 
Gain in-depth insights into sales performance from a power seller's perspective. Track revenue, identify best-selling products, uncover seasonal trends, and assess pricing strategies.

## INPUT: File (CSV fields)
```
Listing Date | Order Date | SKU	Order Id | Listing Title | Department | Category | Subcategory | Brand | Color | Size | Bundle Order? | Offer Order | NWT | Cost Price | Order Price | Seller Shipping Discount | Upgraded Shipping Label Fee | Net Earnings | Buyer State | Buyer Zip Code | Buyer Username | Sales Tax (Paid by Buyer) | Sales Tax (Paid by Seller) | Notes | Other Info		
```
## OUTPUT: Automated Analytics (Examples only due to GDPR)
<img width="775" alt="Dashboard" src="https://github.com/kakun45/resellershelper_sample/assets/53381916/0f617dce-b39b-415f-8980-a0a99b27c97d">

**Few Dashboard Visuals Overview**

Explore the top 10 buyer states to understand your customer base. Use this insight to optimize sourcing, timing, and outreach. Identify tax holidays, exemptions, and geographic patterns. The "Net Earnings" metric is used for mapping accuracy. States with no purchases may appear shaded off. Upon request: to include territories like FM, MH, and PW.
<img width="1173" alt="Map by state" src="https://github.com/kakun45/resellershelper_sample/assets/53381916/39ebae35-dabb-443d-af61-c9fdccf3d00f">
**Geographic Sales Analysis**

Zip-code level maps visualize buyer locations with points sized and colored by purchase value. Some distortion may appear due to resolution (sorry, Puerto Rico!).

![Map by Sz of purchase](https://github.com/kakun45/resellershelper_sample/assets/53381916/e4f733f2-4b73-41b8-9e28-89a9c5fd446c)

**Best-Selling Categories**

Use bar plots to assess strengths and improvement areas. The graph counts individual items sold, including those in bundles, and shows high- and low-performing categories. Top 5 categories are listed. Subcategory data as a customization is available on request.

![CategoryCount2020](https://github.com/kakun45/resellershelper_sample/assets/53381916/2de2e670-8938-4998-939f-d5669ed54b25)

**Unsupervised Learning Insights**

K-means clustering is applied to uncover hidden patterns in your data. Domain knowledge enhances the interpretation of these clusters, which are visualized across key axes.

![kmeansCluster0-N](https://github.com/kakun45/resellershelper_sample/assets/53381916/3c7d196a-e061-4aeb-b6ee-112587f12797)

**Seasonality Trends** 

Multi-level analysis of seasonal trends with aggregation, color-coding and comparisons to spot trends in cycles and spikes.
![scatter plot 3_20](https://github.com/kakun45/resellershelper_sample/assets/53381916/6a7c25ae-d602-4d9b-9a83-c5035b222e90)

**Fee and Cost Advisory**

Did you know that 65% of Americans can't recall what they spent last month? For Fashion resellers, operating on slim margin, this lack of clarity can be costly. Classy Graphs helps you break down Poshmark’s 20% fee structure—and uncover hidden costs that often go unnoticed.

Start by considering your base price (e.g., $15), shipping, bundle discounts, and other expenses. Our data shows that listings priced below $15 often incur more than the standard 20% fee, shrinking your margins. If you offer free shipping, you’re not off the hook—it triggers an extra 20% fee on the label cost, which you pay instead of the buyer.

Use these insights to tailor your pricing strategy and avoid unintentional profit loss. Even in cases where earnings dip into the negative—whether strategically or for tax reasons—knowing your financial boundaries is critical.

Our graph will illustrate two key scenarios of your data: the standard 20% fee and cases where total deductions exceed that—up to 25%, 30%, or even 70%—due to discounts or other adjustments. Bundle configurations are fully customizable. For a true picture of profitability, factor in your COGS, platform fees, shipping, and taxes.

![sr_total_fees_paid](https://github.com/kakun45/resellershelper_sample/assets/53381916/580ae22d-23ae-4950-a4f6-81d44a29b368)
