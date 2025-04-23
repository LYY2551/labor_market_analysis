import excel "Unemployment Rate.xlsx", sheet("Sheet1"cellrange(A1:D49) firstrow

**绘制中美总失业率折线图**
twoway (line total_unemp year if country=="China", lcolor(red)) ///
       (line total_unemp year if country=="USA", lcolor(blue)), ///
       ytitle("Unemployment Rate (%)") ///
       xtitle("Year") ///
       title("China-USA Total Unemployment Rate (2000-2023)") ///
       legend(label(1 "China") label(2 "USA")) ///
       text(3 2008 "2008 Crisis", placement(e)) ///
	   text(2 2018 "2018 Trade War", placement(e)) ///
       text(5 2020 "COVID-19", placement(e))
	   
**绘制中美青年失业率折线图**
twoway (line youth_unemp year if country=="China", lcolor(red)) ///
       (line youth_unemp year if country=="USA", lcolor(blue)), ///
       ytitle("Youth Unemployment Rate (%)") ///
       xtitle("Year") ///
       title("China-USA Youth Unemployment Rate (2000-2023)") ///
       legend(label(1 "China") label(2 "USA")) ///
       text(9 2008 "2008 Crisis", placement(e)) ///
	   text(12 2017 "2018 Trade War", placement(e)) ///
       text(16 2020 "2020 COVID-19", placement(e))