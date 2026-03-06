
import { useState } from "react";

function BacktestPanel() {

  const [result, setResult] = useState(null);

  function runBacktest() {

    fetch("http://localhost:8000/backtest/BTC")
      .then(res => res.json())
      .then(setResult);

  }

  return (

    <div>

      <h2>Strategy Backtester</h2>

      <button onClick={runBacktest}>
        Run Backtest
      </button>

      {result && (

        <div>

          <p>Return: {result.return_pct}%</p>
          <p>Final Value: ${result.final_value}</p>

        </div>

      )}

    </div>

  );

}

export default BacktestPanel;