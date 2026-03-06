
// hooks/useAI.js

import { useState } from "react";
import { aiService } from "../api/aiService";

export function useAI() {
    const [explanations, setExplanations] = useState({});
    const [analyzingSymbol, setAnalyzingSymbol] = useState(null);
    const [analysisResults, setAnalysisResults] = useState({});

    const explain = async (symbol) => {
        try {
            const data = await aiService.explain(symbol);

            setExplanations((prev) => ({
                ...prev,
                [symbol]: data.explanation || "No explanation available.",
            }));
        } catch {
            setExplanations((prev) => ({
                ...prev,
                [symbol]: "Unable to generate explanation.",
            }));
        }
    };

    const analyze = async (symbol) => {
        setAnalyzingSymbol(symbol);

        let result;

        try {
            result = await aiService.analyze({
                symbol,
                portfolio_size: 5000,
                risk_profile: "balanced",
                time_horizon: "short-term",
            });

            return result;

        } catch (error) {
            if (error?.message === "Daily analysis limit reached") {
                throw new Error("LIMIT_REACHED");
            }

            if (error?.message === "Trader Mode required") {
                throw new Error("UPGRADE_REQUIRED");
            }

            throw new Error("ANALYSIS_FAILED");

        } finally {
            setAnalyzingSymbol(null);

            if (result) {
                setAnalysisResults(prev => ({
                    ...prev,
                    [symbol]: result
                }));
            }
        }
    };
    
    return {
        explanations,
        explain,
        analyze,
        analyzingSymbol,
        analysisResults
    };
}