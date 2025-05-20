install_lib <- function(libs) {

    for (lib in libs){
        
        if(!require(lib, character.only = TRUE)){
            
            message <- paste("install packege: ", lib)
            print(message)
            install.packages(lib)
        
        } else {
            
            print("packet alredy had installed")
        }
    }
}

variableFunc <- function(){
    
    libs = c(

        "tidyverse",
        "dynlm",
        "ARDL",
        "RJDemetra", 
        "readr",
        "tseries"

    )

    return(libs)
}

main_installLib <- function(){

    libs <- variableFunc()
    install_lib(libs)
    print("SUCCCESS INSTALL LIB DONE")

}

main_installLib()