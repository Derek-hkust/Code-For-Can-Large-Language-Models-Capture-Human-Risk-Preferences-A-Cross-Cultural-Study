use CleanData, clear
set more off
*********real*********
capture program drop ML_eut

do ML_code_HK
global choice "Choice1 Choice2 Choice3 Choice4 Choice5 Choice6 Choice7 Choice8 Choice9"
global probL "ProbA1LL ProbA2LL ProbA3LL ProbB4LL ProbB5LL ProbB6LL ProbC7LL ProbC8LL ProbC9LL"
global lotR "LotA1R LotA2R LotA3R LotB4R LotB5R LotB6R LotC7R LotC8R LotC9R"

ml model lf ML_eut (r: $choice $probL $lotR=  age gender edu personal_income) (LNmu: =), maximize difficult cluster(Num)
ml display

predictnl ra_real=xb(r), se(sera_real) variance(ravar_real)

*********4o*********
capture program drop ML_eut

do ML_code_HK
global choice "a1 a2 a3 a4 a5 a6 a7 a8 a9"
global probL "ProbA1LL ProbA2LL ProbA3LL ProbB4LL ProbB5LL ProbB6LL ProbC7LL ProbC8LL ProbC9LL"
global lotR "LotA1R LotA2R LotA3R LotB4R LotB5R LotB6R LotC7R LotC8R LotC9R"

ml model lf ML_eut (r: $choice $probL $lotR=  age gender edu personal_income) (LNmu: =), maximize difficult cluster(Num)
ml display

predictnl ra_4o=xb(r), se(sera_4o) variance(ravar_4o)

*********o1-mini*********
capture program drop ML_eut

do ML_code_HK
global choice "b1 b2 b3 b4 b5 b6 b7 b8 b9"
global probL "ProbA1LL ProbA2LL ProbA3LL ProbB4LL ProbB5LL ProbB6LL ProbC7LL ProbC8LL ProbC9LL"
global lotR "LotA1R LotA2R LotA3R LotB4R LotB5R LotB6R LotC7R LotC8R LotC9R"

ml model lf ML_eut (r: $choice $probL $lotR=  age gender edu personal_income) (LNmu: =), maximize difficult cluster(Num)
ml display

predictnl ra_o1=xb(r), se(sera_o1) variance(ravar_o1)

*********4o_CN*********
capture program drop ML_eut

do ML_code_HK
global choice "c_a1 c_a2 c_a3 c_a4 c_a5 c_a6 c_a7 c_a8 c_a9"
global probL "ProbA1LL ProbA2LL ProbA3LL ProbB4LL ProbB5LL ProbB6LL ProbC7LL ProbC8LL ProbC9LL"
global lotR "LotA1R LotA2R LotA3R LotB4R LotB5R LotB6R LotC7R LotC8R LotC9R"

ml model lf ML_eut (r: $choice $probL $lotR=  age gender edu personal_income) (LNmu: =), maximize difficult cluster(Num)
ml display

predictnl Cra_4o=xb(r), se(Csera_4o) variance(Cravar_4o)

*********o1-mini*********
capture program drop ML_eut

do ML_code_HK
global choice "c_b1 c_b2 c_b3 c_b4 c_b5 c_b6 c_b7 c_b8 c_b9"
global probL "ProbA1LL ProbA2LL ProbA3LL ProbB4LL ProbB5LL ProbB6LL ProbC7LL ProbC8LL ProbC9LL"
global lotR "LotA1R LotA2R LotA3R LotB4R LotB5R LotB6R LotC7R LotC8R LotC9R"

ml model lf ML_eut (r: $choice $probL $lotR=  age gender edu personal_income) (LNmu: =), maximize difficult cluster(Num)
ml display

predictnl Cra_o1=xb(r), se(Csera_o1) variance(Cravar_o1)

*********comparison*********
ttest ra_real == ra_4o
ttest ra_real == ra_o1
ttest ra_real == Cra_4o
ttest ra_real == Cra_o1

twoway  (kdensity ra_4o, color(blue)) ///
        (kdensity ra_o1, color(red)) ///
        (kdensity ra_real, color(green)), ///
        legend(label(1 "4o") label(2 "o1-mini") label(3 "Real") rows(1)) ///
        graphregion(color(white)) ///
        ylabel(,nogrid) ///
        xtitle("Values") ytitle("Density")

codebook ra_real ra_4o ra_o1

gen diff4o = ra_real - ra_4o
regress diff4o gender age edu personal_income, robust
gen diffo1 = ra_real - ra_o1
regress ra_o1 gender age edu personal_income, robust
