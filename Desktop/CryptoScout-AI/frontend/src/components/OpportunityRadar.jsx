
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from "recharts";
import { useEffect, useState } from "react";

function OpportunityRadar() {

  const [data, setData] = useState([]);

  useEffect(() => {

    fetch("http://localhost:8000/monitor/opportunity-radar")
      .then(res => res.json())
      .then(setData);

  }, []);

  return (

    <RadarChart width={500} height={400} data={data}>
      <PolarGrid />
      <PolarAngleAxis dataKey="axis" />
      <PolarRadiusAxis />

      <Radar
        name="Opportunities"
        dataKey="value"
        stroke="#00e0ff"
        fill="#00e0ff"
        fillOpacity={0.6}
      />

    </RadarChart>

  );

}

export default OpportunityRadar;