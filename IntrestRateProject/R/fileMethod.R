library(readr)

openCSV <- function(file){
    
    #main function logic
    fileCSV <- read_csv(file)

    #loging
    message <- paste("CSV was write in\n", fileCSV)
    print(message)

    #returning
    return (fileCSV)

}

transform_to_dataSet <- function(file){

    #main function logic
    baseSet <- openCSV(file)
    dataSet <- as.data.frame(baseSet)

    #loging
    message <- paste("CSV file\n", baseSet, "\nwas succefull transformed to DataFrame\n", dataSet)
    print(message) 

    #returning
    return(dataSet)
    
}

plotDraw <- function(file, name){

    file_name = paste0(name, '.png')
    png(file_name, width = 800, height = 600)
    plot(file, main = name, xlab = "date", ylab = "value")
    dev.off()
}

writeCSV <- function(file, name){
    
    name <- paste0(name, ".csv")
    file_open <- file(name, open = "w")
    new_fileCSV <- write.csv(file, name, row.names = FALSE)

    mes <- paste0("CSV file file_name = <", name, "> was succefully write")
    print(mes)

    return(new_fileCSV)
}
