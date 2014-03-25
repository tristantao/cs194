x = 5
setwd("/Users/t-rex-Box/Desktop/work/cs194/lab6/")

nyt1 <- read.csv("nyt1-sample.csv")

nyt1$CTR = nyt1$Clicks / nyt1$Impressions

sum(nyt1$Clicks) / sum(nyt1$Impressions)

attach(mtcars)
head(mtcars)

plot(mpg ~ wt)
hist(mpg)
hist(wt, 10000)
sort(table(wt), decreasing=TRUE)

plot(mpg ~ hp)
model_hp <- lm(mpg ~ hp)
summary(model_hp)
plot(hp, mpg)
abline(model_hp$coefficients)

plot(model_hp$fitted, model_hp$residuals)
abline(h=0, lty=2)
qqnorm(residuals(model_hp))
qqline(residuals(model_hp))

model_all <- lm(mpg ~ cyl + disp+drat+ hp + wt + qsec + vs + am + gear  + carb)
summary(model_all)
plot(fitted(model_all), residuals(model_all))
abline(h=0, lty=2)

model_hp_wt <- lm(mpg ~ hp + wt)
summary(model_hp_wt)
plot(fitted(model_hp_wt), residuals(model_hp_wt))
abline(h=0, lty=2)
anscombe

plot(anscombe$x1, anscombe$y1)
plot(anscombe$x2, anscombe$y2)


lm1 <- lm(y1 ~ x1, data=anscombe)
summary(lm1)
lm2 <- lm(y2 ~ x2, data=anscombe)
summary(lm2)


