"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Image from "next/image";
import { testBills } from "@/test/data/bills";
import { Dialog, Transition } from "@headlessui/react";
import { Fragment } from "react";
import Link from "next/link";

type ConnectedProvider = {
  id: string;
  name: string;
  logo: string;
  connectedAt: string;
};

type StepStatus = "completed" | "current" | "upcoming";

interface Step {
  id: number;
  name: string;
  description: string;
  icon: React.ReactNode;
  status: StepStatus;
}

type LoginModalProps = {
  isOpen: boolean;
  onClose: () => void;
  provider: {
    id: string;
    name: string;
    logo: string;
  };
};

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [isConnecting, setIsConnecting] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [isInsuranceConnected, setIsInsuranceConnected] = useState(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("isInsuranceConnected") === "true";
    }
    return false;
  });
  const [selectedBills, setSelectedBills] = useState<string[]>([]);
  const [connectedProvider, setConnectedProvider] =
    useState<ConnectedProvider | null>(() => {
      if (typeof window !== "undefined") {
        const saved = localStorage.getItem("connectedProvider");
        return saved ? JSON.parse(saved) : null;
      }
      return null;
    });
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisComplete, setAnalysisComplete] = useState(false);
  const [analysisResults, setAnalysisResults] = useState<any>(null);
  const [completedSteps, setCompletedSteps] = useState<number[]>(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("completedSteps");
      return saved ? JSON.parse(saved) : [];
    }
    return [];
  });
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

  console.log("Dashboard auth state:", { user, loading }); // Debug log

  useEffect(() => {
    if (!loading && !user) {
      router.push("/auth");
    }
  }, [user, loading, router]);

  useEffect(() => {
    if (completedSteps.length > 0) {
      const lastCompletedStep = Math.max(...completedSteps);
      setCurrentStep(lastCompletedStep + 1);
    }
  }, [completedSteps]);

  useEffect(() => {
    // If we have a connected provider, start at step 2
    if (isInsuranceConnected && connectedProvider) {
      setCurrentStep(2);
    }
  }, [isInsuranceConnected, connectedProvider]);

  if (loading || !user) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  const handleConnect = () => {
    const provider = insuranceProviders.find((p) => p.id === selectedProvider);
    if (provider) {
      setIsLoginModalOpen(true);
    }
  };

  const handleLoginModalClose = () => {
    setIsLoginModalOpen(false);
    const provider = insuranceProviders.find((p) => p.id === selectedProvider);
    if (provider) {
      const connectedProviderData = {
        id: provider.id,
        name: provider.name,
        logo: provider.logo,
        connectedAt: new Date().toISOString(),
      };
      localStorage.setItem("isInsuranceConnected", "true");
      localStorage.setItem(
        "connectedProvider",
        JSON.stringify(connectedProviderData)
      );
      localStorage.setItem(
        "completedSteps",
        JSON.stringify([...completedSteps, 1])
      );
      setCompletedSteps((prev) => [...prev, 1]);
      setIsInsuranceConnected(true);
      setConnectedProvider(connectedProviderData);
      setCurrentStep(2);
    }
  };

  const handleBillSelect = (billId: string) => {
    setSelectedBills((prev) =>
      prev.includes(billId)
        ? prev.filter((id) => id !== billId)
        : [...prev, billId]
    );
  };

  const handleReset = () => {
    localStorage.removeItem("finishedWelcomeFlow");
    document.cookie =
      "finishedWelcomeFlow=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    localStorage.removeItem("isInsuranceConnected");
    localStorage.removeItem("connectedProvider");
    localStorage.removeItem("completedSteps");
    localStorage.removeItem("importedBills");
    // Reset all state
    setIsInsuranceConnected(false);
    setConnectedProvider(null);
    setCompletedSteps([]);
    setCurrentStep(1);
    setSelectedProvider(null);
    setSelectedBills([]);
    setAnalysisComplete(false);
    setAnalysisResults(null);
  };

  const insuranceProviders = [
    {
      id: "uhc",
      name: "UnitedHealthcare",
      logo: "/images/providers/united.png",
    },
    {
      id: "anthem",
      name: "Anthem Blue Cross",
      logo: "/images/providers/anthem.png",
    },
    {
      id: "aetna",
      name: "Aetna",
      logo: "/images/providers/aetna.png",
    },
    {
      id: "cigna",
      name: "Cigna",
      logo: "/images/providers/cigna.png",
    },
    {
      id: "humana",
      name: "Humana",
      logo: "/images/providers/humana.png",
    },
  ];

  const steps: Step[] = [
    {
      id: 1,
      name: "Connect Insurance",
      description: "Link your insurance provider to get started",
      status: completedSteps.includes(1)
        ? "completed"
        : currentStep === 1
        ? "current"
        : "upcoming",
      icon: (
        <svg
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
          />
        </svg>
      ),
    },
    {
      id: 2,
      name: "Import Bills",
      description: "We'll securely fetch your medical bills and EOBs",
      status: completedSteps.includes(2)
        ? "completed"
        : currentStep === 2
        ? "current"
        : "upcoming",
      icon: (
        <svg
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
      ),
    },
    {
      id: 3,
      name: "Review Savings",
      description: "Discover potential savings in your bills",
      status: completedSteps.includes(3)
        ? "completed"
        : currentStep === 3
        ? "current"
        : "upcoming",
      icon: (
        <svg
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      ),
    },
  ];

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    setTimeout(() => {
      // Get all provider bills
      const allProviderBills =
        testBills[connectedProvider?.id as keyof typeof testBills] || [];

      // Analyze selected bills
      const results = selectedBills.map((billId, index) => {
        const bill = allProviderBills.find((b) => b.id === billId);

        // Calculate savings based on bill amount (roughly 30%)
        const totalAmount = bill?.amount || 0;
        const targetSavings = totalAmount * 0.3;

        // Different analysis patterns based on bill index
        let analysis;
        if (index % 3 === 0) {
          // First pattern: Heavy on duplicate charges
          analysis = {
            duplicateCharges: [
              {
                description: "Lab Test - Complete Blood Count",
                originalAmount: Math.round(totalAmount * 0.15),
                duplicateAmount: Math.round(totalAmount * 0.15),
                potential_saving: Math.round(totalAmount * 0.15),
              },
              {
                description: "Diagnostic Imaging - X-Ray",
                originalAmount: Math.round(totalAmount * 0.1),
                duplicateAmount: Math.round(totalAmount * 0.1),
                potential_saving: Math.round(totalAmount * 0.1),
              },
            ],
            overcharges: [
              {
                description: "Medical Supplies",
                originalAmount: Math.round(totalAmount * 0.1),
                marketRate: Math.round(totalAmount * 0.07),
                potential_saving: Math.round(totalAmount * 0.03),
              },
            ],
            negotiableItems: [
              {
                description: "Facility Fee",
                originalAmount: Math.round(totalAmount * 0.1),
                recommendedAmount: Math.round(totalAmount * 0.08),
                potential_saving: Math.round(totalAmount * 0.02),
              },
            ],
          };
        } else if (index % 3 === 1) {
          // Second pattern: Heavy on overcharges
          analysis = {
            duplicateCharges: [],
            overcharges: [
              {
                description: "Emergency Room Level 4",
                originalAmount: Math.round(totalAmount * 0.45),
                marketRate: Math.round(totalAmount * 0.3),
                potential_saving: Math.round(totalAmount * 0.15),
              },
              {
                description: "CT Scan - With Contrast",
                originalAmount: Math.round(totalAmount * 0.35),
                marketRate: Math.round(totalAmount * 0.25),
                potential_saving: Math.round(totalAmount * 0.1),
              },
            ],
            negotiableItems: [
              {
                description: "Professional Services",
                originalAmount: Math.round(totalAmount * 0.2),
                recommendedAmount: Math.round(totalAmount * 0.15),
                potential_saving: Math.round(totalAmount * 0.05),
              },
            ],
          };
        } else {
          // Third pattern: Heavy on negotiable items
          analysis = {
            duplicateCharges: [],
            overcharges: [
              {
                description: "IV Administration",
                originalAmount: Math.round(totalAmount * 0.15),
                marketRate: Math.round(totalAmount * 0.1),
                potential_saving: Math.round(totalAmount * 0.05),
              },
            ],
            negotiableItems: [
              {
                description: "Room & Board",
                originalAmount: Math.round(totalAmount * 0.4),
                recommendedAmount: Math.round(totalAmount * 0.25),
                potential_saving: Math.round(totalAmount * 0.15),
              },
              {
                description: "Anesthesia Services",
                originalAmount: Math.round(totalAmount * 0.25),
                recommendedAmount: Math.round(totalAmount * 0.15),
                potential_saving: Math.round(totalAmount * 0.1),
              },
            ],
          };
        }

        // Calculate total savings
        const totalSavings =
          analysis.duplicateCharges.reduce(
            (acc, item) => acc + item.potential_saving,
            0
          ) +
          analysis.overcharges.reduce(
            (acc, item) => acc + item.potential_saving,
            0
          ) +
          analysis.negotiableItems.reduce(
            (acc, item) => acc + item.potential_saving,
            0
          );

        return {
          ...bill,
          analysis: {
            ...analysis,
            totalPotentialSavings: totalSavings,
          },
          status: "Imported",
        };
      });

      // Save ALL bills to localStorage, with analysis for selected ones
      const existingBills = JSON.parse(
        localStorage.getItem("importedBills") || "[]"
      );

      const newBills = allProviderBills.map((bill) => ({
        ...bill,
        status: "Imported",
        analysis: selectedBills.includes(bill.id)
          ? results.find((r) => r.id === bill.id)?.analysis
          : undefined,
      }));

      localStorage.setItem(
        "importedBills",
        JSON.stringify([...existingBills, ...newBills])
      );

      setAnalysisResults(results);
      setAnalysisComplete(true);
      setIsAnalyzing(false);
    }, 6000);
  };

  // Add this function to handle step clicks
  const handleStepClick = (stepId: number) => {
    // Only allow going back to completed steps
    if (completedSteps.includes(stepId)) {
      setCurrentStep(stepId);
    }
  };

  // Bills View Component
  const BillsView = () => {
    // Get bills for the connected provider
    const providerBills = connectedProvider
      ? testBills[connectedProvider.id as keyof typeof testBills] || []
      : [];

    if (isAnalyzing) {
      return <AnalysisLoading />;
    }

    if (analysisComplete && analysisResults) {
      return <AnalysisResults results={analysisResults} router={router} />;
    }

    return (
      <div className="space-y-8">
        {/* Connected Provider Info */}
        {connectedProvider && (
          <div className="rounded-lg bg-white p-6 shadow-sm ring-1 ring-gray-100">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="relative h-12 w-24">
                  <Image
                    src={connectedProvider.logo}
                    alt={connectedProvider.name}
                    fill
                    className="object-contain"
                    sizes="100px"
                  />
                </div>
                <div>
                  <h2 className="text-lg font-medium text-gray-900">
                    Connected to {connectedProvider.name}
                  </h2>
                  <p className="text-sm text-gray-500">
                    Connected{" "}
                    {new Date(
                      connectedProvider.connectedAt
                    ).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2 text-sm text-green-600">
                <svg
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span>Active Connection</span>
              </div>
            </div>
          </div>
        )}

        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-medium text-gray-900">
              Your Medical Bills
            </h2>
            <p className="mt-1 text-sm text-gray-500">
              Select the bills you'd like us to analyze
            </p>
          </div>
          {selectedBills.length > 0 && (
            <button
              onClick={handleAnalyze}
              className="inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
            >
              Analyze {selectedBills.length} Bills
            </button>
          )}
        </div>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {providerBills.map((bill) => (
            <div
              key={bill.id}
              onClick={() => handleBillSelect(bill.id)}
              className={`group relative cursor-pointer overflow-hidden rounded-xl border bg-white p-4 transition-all hover:border-blue-500 hover:shadow-md ${
                selectedBills.includes(bill.id)
                  ? "border-blue-500 bg-blue-50 ring-1 ring-blue-500"
                  : "border-gray-200"
              }`}
            >
              <div className="aspect-[3/4] w-full overflow-hidden rounded-lg bg-gray-100">
                <div className="relative h-full w-full">
                  <Image
                    src={bill.thumbnail}
                    alt={bill.description}
                    fill
                    className="object-cover"
                    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                  />
                </div>
              </div>
              <div className="mt-4">
                <div className="flex items-center justify-between">
                  <span
                    className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                      bill.type === "EOB"
                        ? "bg-purple-100 text-purple-800"
                        : "bg-blue-100 text-blue-800"
                    }`}
                  >
                    {bill.type}
                  </span>
                  <span className="text-sm text-gray-500">
                    {new Date(bill.date).toLocaleDateString()}
                  </span>
                </div>
                <h3 className="mt-2 font-medium text-gray-900">
                  {bill.description}
                </h3>
                <p className="mt-1 text-sm text-gray-500">
                  ${bill.amount.toLocaleString()}
                </p>
              </div>
              <div
                className={`absolute right-4 top-4 transition-opacity ${
                  selectedBills.includes(bill.id)
                    ? "opacity-100"
                    : "opacity-0 group-hover:opacity-100"
                }`}
              >
                <div className="rounded-full bg-white p-1 shadow-sm">
                  <svg
                    className={`h-5 w-5 ${
                      selectedBills.includes(bill.id)
                        ? "text-blue-600"
                        : "text-gray-400"
                    }`}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Render bills view if insurance is connected
  if (isInsuranceConnected && (currentStep === 2 || currentStep === 3)) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="relative mx-auto max-w-7xl space-y-10">
          {/* Reset Button - Updated positioning */}
          <div className="flex justify-center sm:justify-end">
            <button
              onClick={handleReset}
              className="inline-flex items-center space-x-2 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-100"
            >
              <svg
                className="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              <span>Reset Progress</span>
            </button>
          </div>
          <div className="mx-auto max-w-7xl space-y-10">
            {/* Progress Steps */}
            <div className="relative mt-12">
              {/* Steps */}
              <div className="relative grid grid-cols-1 gap-8 sm:grid-cols-3 sm:gap-4">
                {steps.map((step) => (
                  <div
                    key={step.id}
                    className={`transition-all duration-300 ${
                      step.status === "completed"
                        ? "opacity-100 cursor-pointer"
                        : step.status === "current"
                        ? "opacity-75"
                        : "opacity-50"
                    }`}
                    onClick={() =>
                      step.status === "completed" && handleStepClick(step.id)
                    }
                  >
                    <div className="flex items-center space-x-4 sm:items-start">
                      <div
                        className={`relative flex h-14 w-14 flex-shrink-0 items-center justify-center rounded-full transition-all duration-300 ${
                          step.status === "completed"
                            ? "bg-green-500 text-white ring-2 ring-green-500 ring-offset-2"
                            : step.status === "current"
                            ? "bg-blue-500 text-white ring-2 ring-blue-500 ring-offset-2"
                            : "bg-white text-gray-400 ring-2 ring-gray-200 ring-offset-2"
                        }`}
                      >
                        {step.status === "completed" ? (
                          <svg
                            className="h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M5 13l4 4L19 7"
                            />
                          </svg>
                        ) : (
                          step.icon
                        )}
                        <span className="absolute -bottom-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-white text-xs font-medium text-gray-900 ring-2 ring-white">
                          {step.id}
                        </span>
                      </div>
                      <div className="flex-1 pt-1 sm:pt-2">
                        <h3
                          className={`font-medium transition-colors ${
                            step.status === "completed"
                              ? "text-gray-900"
                              : step.status === "current"
                              ? "text-gray-900"
                              : "text-gray-500"
                          }`}
                        >
                          {step.name}
                        </h3>
                        <p
                          className={`mt-1 text-sm transition-colors ${
                            step.status === "completed"
                              ? "text-gray-600"
                              : step.status === "current"
                              ? "text-gray-600"
                              : "text-gray-400"
                          }`}
                        >
                          {step.description}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Bills Selection or Analysis Results */}
            <BillsView />
          </div>
        </div>
      </div>
    );
  }

  // Original return for step 1
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="relative mx-auto max-w-7xl space-y-10">
        {/* Reset Button - Updated positioning */}
        <div className="flex justify-center sm:justify-end">
          <button
            onClick={handleReset}
            className="inline-flex items-center space-x-2 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-100"
          >
            <svg
              className="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
            <span>Reset Progress</span>
          </button>
        </div>
        <div className="mx-auto max-w-4xl space-y-10">
          {/* Welcome Section */}
          <div className="text-center">
            <h1 className="text-3xl font-medium text-gray-900">
              Welcome to a simpler healthcare experience
            </h1>
            <p className="mt-3 text-lg text-gray-600">
              Let's connect your insurance and start saving on your medical
              bills
            </p>
          </div>

          {/* Modern Progress Steps */}
          <div className="relative mt-12">
            {/* Steps */}
            <div className="relative grid grid-cols-1 gap-8 sm:grid-cols-3 sm:gap-4">
              {steps.map((step) => (
                <div
                  key={step.id}
                  className={`transition-all duration-300 ${
                    step.status === "completed"
                      ? "opacity-100 cursor-pointer"
                      : step.status === "current"
                      ? "opacity-75"
                      : "opacity-50"
                  }`}
                  onClick={() =>
                    step.status === "completed" && handleStepClick(step.id)
                  }
                >
                  <div className="flex items-center space-x-4 sm:items-start">
                    <div
                      className={`relative flex h-14 w-14 flex-shrink-0 items-center justify-center rounded-full transition-all duration-300 ${
                        step.status === "completed"
                          ? "bg-green-500 text-white ring-2 ring-green-500 ring-offset-2"
                          : step.status === "current"
                          ? "bg-blue-500 text-white ring-2 ring-blue-500 ring-offset-2"
                          : "bg-white text-gray-400 ring-2 ring-gray-200 ring-offset-2"
                      }`}
                    >
                      {step.status === "completed" ? (
                        <svg
                          className="h-6 w-6"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                      ) : (
                        step.icon
                      )}
                      <span className="absolute -bottom-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-white text-xs font-medium text-gray-900 ring-2 ring-white">
                        {step.id}
                      </span>
                    </div>
                    <div className="flex-1 pt-1 sm:pt-2">
                      <h3
                        className={`font-medium transition-colors ${
                          step.status === "completed"
                            ? "text-gray-900"
                            : step.status === "current"
                            ? "text-gray-900"
                            : "text-gray-500"
                        }`}
                      >
                        {step.name}
                      </h3>
                      <p
                        className={`mt-1 text-sm transition-colors ${
                          step.status === "completed"
                            ? "text-gray-600"
                            : step.status === "current"
                            ? "text-gray-600"
                            : "text-gray-400"
                        }`}
                      >
                        {step.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Provider Selection */}
          <div className="overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-gray-100">
            <div className="p-8">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-medium text-gray-900">
                    Step 1: Select your insurance provider
                  </h2>
                  <p className="mt-1 text-sm text-gray-500">
                    Choose your provider to begin the connection process
                  </p>
                </div>
                <span className="inline-flex items-center rounded-full bg-blue-50 px-3 py-0.5 text-sm font-medium text-blue-700">
                  Step 1 of 3
                </span>
              </div>

              <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-5">
                {insuranceProviders.map((provider) => (
                  <button
                    key={provider.id}
                    onClick={() => setSelectedProvider(provider.id)}
                    className={`group relative flex flex-col items-center rounded-xl p-4 transition-all hover:bg-gray-50 ${
                      selectedProvider === provider.id
                        ? "ring-2 ring-blue-500"
                        : "ring-1 ring-gray-200"
                    }`}
                  >
                    <div className="relative h-12 w-24">
                      <Image
                        src={provider.logo}
                        alt={provider.name}
                        fill
                        className="object-contain"
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                      />
                    </div>
                  </button>
                ))}
              </div>

              {selectedProvider && (
                <div className="mt-8 flex flex-col items-center">
                  <button
                    onClick={handleConnect}
                    disabled={isConnecting}
                    className="relative inline-flex w-full max-w-md items-center justify-center overflow-hidden rounded-xl bg-gradient-to-r from-blue-500 to-indigo-500 px-8 py-3 text-white shadow-sm transition-all hover:from-blue-600 hover:to-indigo-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
                  >
                    {isConnecting ? (
                      <div className="flex items-center space-x-2">
                        <svg
                          className="h-5 w-5 animate-spin"
                          viewBox="0 0 24 24"
                          fill="none"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          />
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          />
                        </svg>
                        <span>Connecting...</span>
                      </div>
                    ) : (
                      <span className="text-base font-medium">
                        Connect to{" "}
                        {
                          insuranceProviders.find(
                            (p) => p.id === selectedProvider
                          )?.name
                        }
                      </span>
                    )}
                  </button>
                  <p className="mt-3 text-sm text-gray-500">
                    You'll be securely redirected to sign in
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Next Steps Preview */}
          {/* <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-xl bg-gray-50 p-6">
              <div className="flex items-center space-x-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-200 text-sm font-medium text-gray-600">
                  2
                </span>
                <h3 className="text-lg font-medium text-gray-900">
                  Coming Next: Import Bills
                </h3>
              </div>
              <p className="mt-2 text-sm text-gray-600">
                After connecting, we'll automatically import your medical bills
                and EOBs for analysis
              </p>
            </div>
            <div className="rounded-xl bg-gray-50 p-6">
              <div className="flex items-center space-x-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-200 text-sm font-medium text-gray-600">
                  3
                </span>
                <h3 className="text-lg font-medium text-gray-900">
                  Then: Review Savings
                </h3>
              </div>
              <p className="mt-2 text-sm text-gray-600">
                We'll analyze your bills and show you potential savings
                opportunities
              </p>
            </div>
          </div> */}

          {/* Trust Badge */}
          <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
            <svg
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
              />
            </svg>
            <span>Your data is protected with bank-level security</span>
          </div>
        </div>
      </div>
      {selectedProvider && (
        <LoginModal
          isOpen={isLoginModalOpen}
          onClose={handleLoginModalClose}
          provider={insuranceProviders.find((p) => p.id === selectedProvider)!}
        />
      )}
    </div>
  );
}

const AnalysisLoading = () => (
  <div className="flex min-h-[400px] flex-col items-center justify-center">
    <div className="relative h-24 w-24">
      <div className="absolute h-full w-full animate-pulse rounded-full bg-blue-100"></div>
      <div className="absolute left-1/2 top-1/2 h-16 w-16 -translate-x-1/2 -translate-y-1/2">
        <svg
          className="h-full w-full animate-spin text-blue-500"
          viewBox="0 0 24 24"
        >
          <path
            className="opacity-25"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            fill="currentColor"
          />
        </svg>
      </div>
    </div>
    <h3 className="mt-4 text-lg font-medium text-gray-900">Analyzing Bills</h3>
    <p className="mt-2 text-sm text-gray-500">
      We're reviewing your bills for potential savings...
    </p>
  </div>
);

const AnalysisResults = ({
  results,
  router,
}: {
  results: any[];
  router: any;
}) => {
  const handleStartSavings = () => {
    // Store in both localStorage and cookies for middleware access
    localStorage.setItem("finishedWelcomeFlow", "true");
    document.cookie = "finishedWelcomeFlow=true; path=/";

    // Update bill statuses in localStorage
    const existingBills = JSON.parse(
      localStorage.getItem("importedBills") || "[]"
    );

    // Update status to "Negotiating" for bills that were analyzed
    const updatedBills = existingBills.map((bill: any) => ({
      ...bill,
      status: results.find((r) => r.id === bill.id)
        ? "Negotiating"
        : bill.status,
    }));

    localStorage.setItem("importedBills", JSON.stringify(updatedBills));
    router.push("/dashboard");
  };

  return (
    <div className="space-y-12">
      {/* Total Savings Card - Made larger and more prominent */}
      <div className="overflow-hidden rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 shadow-lg">
        <div className="px-8 py-10">
          <div className="flex flex-col items-center text-center">
            <h3 className="text-xl font-medium text-white">
              Total Potential Savings
            </h3>
            <p className="mt-2 text-4xl font-bold text-white">
              $
              {results
                .reduce(
                  (acc, bill) => acc + bill.analysis.totalPotentialSavings,
                  0
                )
                .toLocaleString()}
            </p>
            <p className="mt-2 text-blue-100">
              We found several opportunities to reduce your costs across{" "}
              {results.length} bills
            </p>
            <div className="mt-6 flex items-center space-x-4">
              <button
                onClick={handleStartSavings}
                className="inline-flex items-center rounded-lg bg-white px-6 py-3 text-base font-medium text-blue-600 shadow-sm hover:bg-blue-50"
              >
                Start Savings Process
              </button>
              <Link
                href="/dashboard"
                onClick={() => {
                  localStorage.setItem("finishedWelcomeFlow", "true");
                  document.cookie = "finishedWelcomeFlow=true; path=/";
                }}
                className="inline-flex items-center rounded-lg border border-white px-6 py-3 text-base font-medium text-white hover:bg-blue-700/20"
              >
                Back to Dashboard
              </Link>
            </div>
          </div>
        </div>
        <div className="bg-blue-700 bg-opacity-40 px-8 py-4">
          <div className="flex items-center justify-center space-x-8 text-sm text-blue-100">
            <div className="flex items-center">
              <svg
                className="mr-2 h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>AI-Powered Analysis</span>
            </div>
            <div className="flex items-center">
              <svg
                className="mr-2 h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>Negotiation Ready</span>
            </div>
          </div>
        </div>
      </div>

      {/* Bills Analysis Section */}
      <div className="space-y-6">
        <h2 className="text-xl font-medium text-gray-900">
          Detailed Analysis by Bill
        </h2>

        {results.map((bill) => (
          <div
            key={bill.id}
            className="overflow-hidden rounded-xl bg-white shadow-sm ring-1 ring-gray-100"
          >
            {/* Bill Header */}
            <div className="border-b border-gray-200 bg-gray-50 px-6 py-4">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center space-x-3">
                    <h4 className="text-lg font-medium text-gray-900">
                      {bill.description}
                    </h4>
                    <span
                      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                        bill.type === "EOB"
                          ? "bg-purple-100 text-purple-800"
                          : "bg-blue-100 text-blue-800"
                      }`}
                    >
                      {bill.type}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500">
                    Original Amount: ${bill.amount.toLocaleString()}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-gray-500">
                    Potential Savings
                  </div>
                  <div className="text-2xl font-bold text-green-600">
                    ${bill.analysis.totalPotentialSavings.toLocaleString()}
                  </div>
                </div>
              </div>
            </div>

            {/* Findings Grid */}
            <div className="grid gap-6 p-6 md:grid-cols-2 lg:grid-cols-3">
              {/* Duplicate Charges */}
              {bill.analysis.duplicateCharges.length > 0 && (
                <div className="rounded-lg border border-red-100 bg-red-50 p-4">
                  <h5 className="flex items-center text-sm font-medium text-red-800">
                    <svg
                      className="mr-2 h-4 w-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 4v16m8-8H4"
                      />
                    </svg>
                    Duplicate Charges Found
                  </h5>
                  <div className="mt-3 space-y-2">
                    {bill.analysis.duplicateCharges.map(
                      (charge: any, idx: number) => (
                        <div
                          key={idx}
                          className="rounded-md bg-white p-3 shadow-sm"
                        >
                          <p className="font-medium text-gray-900">
                            {charge.description}
                          </p>
                          <div className="mt-1 flex items-center justify-between text-sm">
                            <span className="text-red-600">Charged Twice</span>
                            <span className="font-medium text-red-600">
                              ${charge.originalAmount.toLocaleString()}
                            </span>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}

              {/* Above Market Rate */}
              {bill.analysis.overcharges.length > 0 && (
                <div className="rounded-lg border border-orange-100 bg-orange-50 p-4">
                  <h5 className="flex items-center text-sm font-medium text-orange-800">
                    <svg
                      className="mr-2 h-4 w-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                      />
                    </svg>
                    Above Market Rate
                  </h5>
                  <div className="mt-3 space-y-2">
                    {bill.analysis.overcharges.map(
                      (charge: any, idx: number) => (
                        <div
                          key={idx}
                          className="rounded-md bg-white p-3 shadow-sm"
                        >
                          <p className="font-medium text-gray-900">
                            {charge.description}
                          </p>
                          <div className="mt-2 space-y-1 text-sm">
                            <div className="flex justify-between">
                              <span className="text-orange-600">
                                Current Rate
                              </span>
                              <span className="font-medium text-orange-600">
                                ${charge.originalAmount.toLocaleString()}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-green-600">
                                Market Rate
                              </span>
                              <span className="font-medium text-green-600">
                                ${charge.marketRate.toLocaleString()}
                              </span>
                            </div>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}

              {/* Negotiation Opportunities */}
              {bill.analysis.negotiableItems.length > 0 && (
                <div className="rounded-lg border border-blue-100 bg-blue-50 p-4">
                  <h5 className="flex items-center text-sm font-medium text-blue-800">
                    <svg
                      className="mr-2 h-4 w-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"
                      />
                    </svg>
                    Negotiation Opportunities
                  </h5>
                  <div className="mt-3 space-y-2">
                    {bill.analysis.negotiableItems.map(
                      (item: any, idx: number) => (
                        <div
                          key={idx}
                          className="rounded-md bg-white p-3 shadow-sm"
                        >
                          <p className="font-medium text-gray-900">
                            {item.description}
                          </p>
                          <div className="mt-2 space-y-1 text-sm">
                            <div className="flex justify-between">
                              <span className="text-gray-600">
                                Current Amount
                              </span>
                              <span className="font-medium text-gray-600">
                                ${item.originalAmount.toLocaleString()}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-blue-600">
                                Target Amount
                              </span>
                              <span className="font-medium text-blue-600">
                                ${item.recommendedAmount.toLocaleString()}
                              </span>
                            </div>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const LoginModal = ({ isOpen, onClose, provider }: LoginModalProps) => {
  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-2xl transform overflow-hidden rounded-2xl bg-white p-6 shadow-xl transition-all">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="relative h-10 w-20">
                      <Image
                        src={provider.logo}
                        alt={provider.name}
                        fill
                        className="object-contain"
                        sizes="80px"
                      />
                    </div>
                    <Dialog.Title
                      as="h3"
                      className="text-lg font-medium text-gray-900"
                    >
                      Connect to {provider.name}
                    </Dialog.Title>
                  </div>
                  <button
                    onClick={onClose}
                    className="rounded-full p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-500"
                  >
                    <svg
                      className="h-6 w-6"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>

                <div className="mt-6 space-y-4">
                  <div className="rounded-lg bg-gray-50 p-4">
                    <p className="text-sm text-gray-600">
                      For demo purposes, just click outside or the X to simulate
                      a successful connection.
                    </p>
                  </div>

                  <div className="rounded-lg border p-6">
                    <div className="space-y-4">
                      <div>
                        <label
                          htmlFor="username"
                          className="block text-sm font-medium text-gray-700"
                        >
                          Username
                        </label>
                        <input
                          type="text"
                          id="username"
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                          placeholder="Enter your username"
                        />
                      </div>
                      <div>
                        <label
                          htmlFor="password"
                          className="block text-sm font-medium text-gray-700"
                        >
                          Password
                        </label>
                        <input
                          type="password"
                          id="password"
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                          placeholder="Enter your password"
                        />
                      </div>
                      <button className="w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
                        Sign In
                      </button>
                    </div>
                  </div>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
};
