import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://acit3855-lab6.westus3.cloudapp.azure.com`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 10000); // Update every 10 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Health Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Health</th>
						</tr>
						<tr>
							<td colspan="2">Receiver: {stats['receiver']}</td>
						</tr>
						<tr>
							<td colspan="2">Storage: {stats['storage']}</td>
						</tr>
						<tr>
							<td colspan="2">Processing: {stats['processing']}</td>
						</tr>
						<tr>
							<td colspan="2">Audit: {stats['audit']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_update']}</h3>
            </div>
        )
    }
}