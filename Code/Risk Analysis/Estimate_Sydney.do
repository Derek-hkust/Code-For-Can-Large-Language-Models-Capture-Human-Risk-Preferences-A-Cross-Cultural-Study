use CleanData, clear
set more off
*********real*********
capture program drop ML_eut

do ML_code_Sydney
global choice "ChoiceA1 ChoiceA2 ChoiceA3 ChoiceB4 ChoiceB5 ChoiceB6 ChoiceC7 ChoiceC8 ChoiceC9"
global probL "ProbA1LL ProbA2LL ProbA3LL ProbB4LL ProbB5LL ProbB6LL ProbC7LL ProbC8LL ProbC9LL"
global lotR "LotA1R LotA2R LotA3R LotB4R LotB5R LotB6R LotC7R LotC8R LotC9R"

ml model lf ML_eut (r: $choice $probL $lotR =  incHH Gender Age Educ) (LNmu: =), maximize difficult cluster(sNo)
ml display

predictnl ra_real=xb(r), se(sera_real) variance(ravar_real)


*********4o*********
capture program drop ML_eut

do ML_code_Sydney
global choice "a1 a2 a3 a4 a5 a6 a7 a8 a9"
global probL "ProbA1LL ProbA2LL ProbA3LL ProbB4LL ProbB5LL ProbB6LL ProbC7LL ProbC8LL ProbC9LL"
global lotR "LotA1R LotA2R LotA3R LotB4R LotB5R LotB6R LotC7R LotC8R LotC9R"

ml model lf ML_eut (r: $choice $probL $lotR =  incHH Gender Age Educ) (LNmu: =), maximize difficult cluster(sNo)
ml display

predictnl ra_4o=xb(r), se(sera_4o) variance(ravar_4o)

*********o1-mini*********
capture program drop ML_eut

do ML_code_Sydney
global choice "b1 b2 b3 b4 b5 b6 b7 b8 b9"
global probL "ProbA1LL ProbA2LL ProbA3LL ProbB4LL ProbB5LL ProbB6LL ProbC7LL ProbC8LL ProbC9LL"
global lotR "LotA1R LotA2R LotA3R LotB4R LotB5R LotB6R LotC7R LotC8R LotC9R"

ml model lf ML_eut (r: $choice $probL $lotR =  incHH Gender Age Educ) (LNmu: =), maximize difficult cluster(sNo)
ml display

predictnl ra_o1=xb(r), se(sera_o1) variance(ravar_o1)

*********comparison*********
ttest ra_real == ra_4o
ttest ra_real == ra_o1

twoway  (kdensity ra_4o, color(blue)) ///
        (kdensity ra_o1, color(red)) ///
        (kdensity ra_real, color(green)), ///
        legend(label(1 "4o") label(2 "o1-mini") label(3 "Real") rows(1)) ///
        graphregion(color(white)) ///
        ylabel(,nogrid) ///
        xtitle("Values") ytitle("Density")

codebook ra_real ra_4o ra_o1
