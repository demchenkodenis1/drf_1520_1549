import React from "react";

const NotFound404= ({location}) =>{
    return(
        <div>
            <h1> Page not found '{location.pathname}'</h1>
        </div>
    )
}

export default  NotFound404