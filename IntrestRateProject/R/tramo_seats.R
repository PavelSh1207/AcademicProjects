library(RJDemetra)
library(tseries)
source('fileMethod.R', chdir = TRUE)

dataInit <- function(file){

    dataSet <- transform_to_dataSet(file)

    return(dataSet)

}

tramo_seats <- function(file, dateStart, frequency){

    #init parmaeters
    dataSet <- dataInit(file)
    col_names <- colnames(dataSet)
    tramoBox = list()


    for (col in col_names[-1]){

        #core
        timeSeries <- ts(dataSet[[col]], start = dateStart, frequency = frequency)
        adf_test <- adf.test(timeSeries)
        result <- tramoseats(timeSeries, spec = "RSAfull")

        #log
        mes = paste0("adf for col ", col, " is ", adf_test)
        print(mes)
        mes = paste0("model column <", col,">\n", result)
        print(mes)

        #generate plot
        plot_name = paste0("tramoseats_full_", col)
        plotDraw(result, plot_name)

        #result saving
        tramoBox[col] <- result
    }

    #returning result
    return(tramoBox)

}

tramo_anlytics_trend <- function(file, dateStart, frequency){
    
    #init parmaeters
    dataSet <- dataInit(file)
    col_names <- colnames(dataSet)[-1]
    tramoBox = list()

    for(col in col_names){
        
        #data init
        timeSeries <- ts(dataSet[[col]], start = dateStart, frequency = frequency)
        adf_test <- adf.test(timeSeries)

        #core
        result <- tramoseats(timeSeries, spec = "RSAfull")
        result <- result$final$series

        #generate plot
        plot_name = paste0("tramoseats_clear_(trend)_", col)
        plotDraw(result, plot_name)    

        #result saving
        tramoBox[col] <- result

        #log
        mes = paste0("adf for col ", col, " is ", adf_test)
        print(mes)
        mes = paste0("model column <", col,">\n", result)
        print(mes)

        #write to csv
        csvName = paste0("clear_trend_model_tramo_", col, "_.csv")
        write.csv(result, csvName, row.names = FALSE)                    
    }

    #returning result
    return(tramoBox)
        
}



main <- function(){

    start_time <- Sys.time()

    sink("full_logs.csv", split = TRUE)

    models <- tramo_seats(file = "mainDataSet.csv", dateStart = c(2010, 1), frequency = 12)
    model_seasonal <- tramo_anlytics_trend(file = "mainDataSet.csv", dateStart = c(2010, 1), frequency = 12)

    print(models)
    print(model_seasonal)

    end_time <- Sys.time()

    time_work <- end_time - start_time
    mes <- paste0("\nPROGRAM WORKING TIME == ", time_work)
    print(mes)

    sink()

}

main()


