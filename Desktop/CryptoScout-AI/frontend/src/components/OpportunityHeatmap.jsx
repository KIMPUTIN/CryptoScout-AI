
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";

import { useEffect, useState } from "react";

function OpportunityHeatmap() {

  const [data, setData] = useState([]);

  useEffect(() => {

    fetch("http://localhost:8000/monitor/opportunity-heatmap")
      .then(res => res.json())
      .then(setData);

  }, []);

  return (

    <ScatterChart width={600} height={400}>

      <CartesianGrid />

      <XAxis
        type="number"
        dataKey="market_cap"
        name="Market Cap"
      />

      <YAxis
        type="number"
        dataKey="momentum"
        name="Momentum"
      />

      <Tooltip cursor={{ strokeDasharray: "3 3" }} />

      <Scatter
        name="Opportunities"
        data={data}
        fill="#00e0ff"
      />

    </ScatterChart>

  );

}

export default OpportunityHeatmap;