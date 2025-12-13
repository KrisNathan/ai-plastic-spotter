export interface AnalysisResult {
    label: string;
    confidence: number;
    gemini: {
        description: string;
        action: string;
    };
}

export const analyzeImage = async (file: File): Promise<AnalysisResult> => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Failed to analyze image");
    }

    return response.json();
};
