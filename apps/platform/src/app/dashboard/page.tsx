"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState, Fragment } from "react";
import Image from "next/image";
import Link from "next/link";

type Bill = {
  id: string;
  type: "EOB" | "Bill";
  provider: string;
  date: string;
  amount: number;
  description: string;
  status: "Imported" | "Analyzed" | "Negotiating" | "Completed";
  analysis?: {
    duplicateCharges: Array<{
      description: string;
      originalAmount: number;
      duplicateAmount: number;
      potential_saving: number;
    }>;
    overcharges: Array<{
      description: string;
      originalAmount: number;
      marketRate: number;
      potential_saving: number;
    }>;
    negotiableItems: Array<{
      description: string;
      originalAmount: number;
      recommendedAmount: number;
      potential_saving: number;
    }>;
    totalPotentialSavings: number;
    savingsBuckets: {
      duplicateSavings: number;
      marketRateSavings: number;
      additionalSavings: number;
    };
  };
};

type ConnectedProvider = {
  id: string;
  name: string;
  logo: string;
  connectedAt: string;
};

const calculatePotentialSavings = (bills: Bill[]): number => {
  return bills.reduce((total, bill) => {
    if (!bill.analysis) return total;

    const duplicateSavings = bill.analysis.duplicateCharges.reduce(
      (sum, charge) => sum + charge.duplicateAmount,
      0
    );

    const overchargeSavings = bill.analysis.overcharges.reduce(
      (sum, charge) => sum + (charge.originalAmount - charge.marketRate),
      0
    );

    const negotiableSavings = bill.analysis.negotiableItems.reduce(
      (sum, item) => sum + (item.originalAmount - item.recommendedAmount),
      0
    );

    return total + duplicateSavings + overchargeSavings + negotiableSavings;
  }, 0);
};

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [bills, setBills] = useState<Bill[]>(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("savedBills");
      return saved ? (JSON.parse(saved) as Bill[]) : [];
    }
    return [];
  });
  const [connectedProvider, setConnectedProvider] =
    useState<ConnectedProvider | null>(() => {
      if (typeof window !== "undefined") {
        const saved = localStorage.getItem("connectedProvider");
        return saved ? (JSON.parse(saved) as ConnectedProvider) : null;
      }
      return null;
    });
  const [importedBills, setImportedBills] = useState<Bill[]>(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("importedBills");
      return saved ? (JSON.parse(saved) as Bill[]) : [];
    }
    return [];
  });
  const [analyzingBills, setAnalyzingBills] = useState<string[]>([]);
  const [expandedBills, setExpandedBills] = useState<string[]>([]);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/auth");
    }
  }, [user, loading, router]);

  const startSavingsProcess = (billIds: string[]) => {
    const updatedBills = bills.map((bill) =>
      billIds.includes(bill.id)
        ? { ...bill, status: "Negotiating" as const }
        : bill
    );
    setBills(updatedBills);
    localStorage.setItem("savedBills", JSON.stringify(updatedBills));
  };

  const startNegotiation = (billId: string) => {
    const updatedBills = importedBills.map((bill) =>
      bill.id === billId ? { ...bill, status: "Negotiating" as const } : bill
    );
    setImportedBills(updatedBills);
    localStorage.setItem("importedBills", JSON.stringify(updatedBills));
  };

  const analyzeBill = (billId: string) => {
    setAnalyzingBills((prev) => [...prev, billId]);

    setTimeout(() => {
      const updatedBills = importedBills.map((bill) => {
        if (bill.id === billId) {
          // Create the base analysis object
          const baseAnalysis = {
            duplicateCharges: [
              {
                description: "Lab Test - Complete Blood Count",
                originalAmount: 53,
                duplicateAmount: 53,
                potential_saving: 53,
              },
              {
                description: "Diagnostic Imaging - X-Ray",
                originalAmount: 35,
                duplicateAmount: 35,
                potential_saving: 35,
              },
            ],
            overcharges: [
              {
                description: "Medical Supplies",
                originalAmount: 35,
                marketRate: 25,
                potential_saving: 35 - 25,
              },
            ],
            negotiableItems: [
              {
                description: "Facility Fee",
                originalAmount: 35,
                recommendedAmount: 28,
                potential_saving: 35 - 28,
              },
            ],
          };

          // Calculate savings buckets
          const duplicateSavings = baseAnalysis.duplicateCharges.reduce(
            (sum, charge) => sum + charge.duplicateAmount,
            0
          );
          const marketRateSavings = baseAnalysis.overcharges.reduce(
            (sum, charge) => sum + (charge.originalAmount - charge.marketRate),
            0
          );
          const additionalSavings = baseAnalysis.negotiableItems.reduce(
            (sum, item) => sum + (item.originalAmount - item.recommendedAmount),
            0
          );

          // Create the complete analysis object
          const analysis = {
            ...baseAnalysis,
            savingsBuckets: {
              duplicateSavings,
              marketRateSavings,
              additionalSavings,
            },
            totalPotentialSavings:
              duplicateSavings + marketRateSavings + additionalSavings,
          };

          return {
            ...bill,
            status: "Analyzed" as const,
            analysis,
          };
        }
        return bill;
      });

      setImportedBills(updatedBills);
      localStorage.setItem("importedBills", JSON.stringify(updatedBills));
      setAnalyzingBills((prev) => prev.filter((id) => id !== billId));
    }, 2000);
  };

  const toggleBillExpansion = (billId: string) => {
    setExpandedBills((prev) =>
      prev.includes(billId)
        ? prev.filter((id) => id !== billId)
        : [...prev, billId]
    );
  };

  const totalSavings = calculatePotentialSavings(importedBills);

  if (loading || !user) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="mx-auto max-w-7xl space-y-10">
        {/* Connected Provider Info */}
        {connectedProvider && (
          <div className="rounded-lg bg-white p-6 shadow-sm ring-1 ring-gray-100">
            <div className="flex flex-col space-y-4 sm:flex-row sm:items-center sm:justify-between sm:space-y-0">
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
              <Link
                href="/welcome"
                onClick={() => {
                  const currentSteps = JSON.parse(
                    localStorage.getItem("completedSteps") || "[]"
                  );
                  localStorage.setItem(
                    "completedSteps",
                    JSON.stringify(Array.from(new Set([...currentSteps, 1])))
                  );
                }}
                className="flex w-full justify-center sm:w-auto rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
              >
                Import More Bills
              </Link>
            </div>
          </div>
        )}

        {/* Bills Section */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-medium text-gray-900">
                Your Medical Bills
              </h2>
              <p className="mt-1 text-sm text-gray-500">
                Track and manage your healthcare expenses
              </p>
            </div>
          </div>

          {/* Bills Table */}
          <div className="overflow-hidden rounded-lg border border-gray-200 bg-white">
            {/* Mobile View */}
            <div className="block sm:hidden">
              {importedBills.map((bill) => (
                <div key={bill.id} className="border-b border-gray-200 p-4">
                  <div
                    className="cursor-pointer"
                    onClick={() => toggleBillExpansion(bill.id)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <svg
                          className={`h-5 w-5 text-gray-400 transition-transform ${
                            expandedBills.includes(bill.id) ? "rotate-180" : ""
                          }`}
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 9l-7 7-7-7"
                          />
                        </svg>
                        <div>
                          <div className="font-medium text-gray-900">
                            {bill.description}
                          </div>
                          <div className="text-sm text-gray-500">
                            ${bill.amount.toLocaleString()}
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <span
                          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                            bill.status === "Negotiating"
                              ? "bg-yellow-100 text-yellow-800"
                              : bill.status === "Analyzed"
                                ? "bg-blue-100 text-blue-800"
                                : bill.status === "Completed"
                                  ? "bg-green-100 text-green-800"
                                  : "bg-gray-100 text-gray-800"
                          }`}
                        >
                          {bill.status}
                        </span>
                        {bill.analysis?.totalPotentialSavings && (
                          <div className="mt-1 text-sm font-medium text-green-600">
                            $
                            {bill.analysis.totalPotentialSavings.toLocaleString()}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  {/* Expanded content remains the same */}
                  {expandedBills.includes(bill.id) && (
                    <div className="mt-4 space-y-4">
                      {/* Bill Summary Section */}
                      <div className="mb-6 rounded-lg border border-gray-200 bg-white p-4">
                        <div className="flex flex-col space-y-4 sm:flex-row sm:items-center sm:justify-between sm:space-y-0">
                          <div>
                            <h4 className="text-lg font-medium text-gray-900">
                              {bill.description}
                            </h4>
                            <span className="mt-1 block text-sm text-gray-500 sm:mt-0 sm:ml-2 sm:inline">
                              Original Amount: ${bill.amount.toLocaleString()}
                            </span>
                          </div>
                          <div className="text-left sm:text-right">
                            <div className="text-sm font-medium text-gray-500">
                              Potential Savings
                            </div>
                            <div className="text-2xl font-bold text-green-600">
                              $
                              {bill.analysis?.totalPotentialSavings.toLocaleString()}
                            </div>
                          </div>
                        </div>

                        {/* Services and Details Grid */}
                        <div className="mt-4 grid gap-6 border-t border-gray-100 pt-4 sm:grid-cols-2">
                          <div>
                            <h5 className="text-sm font-medium text-gray-700">
                              Services Provided
                            </h5>
                            <ul className="mt-2 space-y-1">
                              {bill.analysis?.duplicateCharges?.map(
                                (charge) => (
                                  <li
                                    key={charge.description}
                                    className="text-sm text-gray-600"
                                  >
                                    • {charge.description} - $
                                    {charge.originalAmount.toLocaleString()}
                                  </li>
                                )
                              )}
                              {bill.analysis?.overcharges?.map((charge) => (
                                <li
                                  key={charge.description}
                                  className="text-sm text-gray-600"
                                >
                                  • {charge.description} - $
                                  {charge.originalAmount.toLocaleString()}
                                </li>
                              ))}
                              {bill.analysis?.negotiableItems?.map((item) => (
                                <li
                                  key={item.description}
                                  className="text-sm text-gray-600"
                                >
                                  • {item.description} - $
                                  {item.originalAmount.toLocaleString()}
                                </li>
                              ))}
                            </ul>
                          </div>
                          <div>
                            <h5 className="text-sm font-medium text-gray-700">
                              Bill Details
                            </h5>
                            <div className="mt-2 space-y-1 text-sm text-gray-600">
                              <div>
                                Date of Service:{" "}
                                {new Date(bill.date).toLocaleDateString(
                                  "en-US",
                                  {
                                    month: "short",
                                    day: "numeric",
                                    year: "numeric",
                                  }
                                )}
                              </div>
                              <div>Bill Type: {bill.type}</div>
                              <div>Provider: {bill.provider}</div>
                              <div>Status: {bill.status}</div>
                            </div>
                          </div>
                        </div>

                        {/* Move Negotiation Opportunities here */}
                        <div className="mt-6 border-t border-gray-100 pt-6">
                          <h4 className="mb-4 text-lg font-medium text-gray-900">
                            Negotiation Opportunities
                          </h4>
                          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                            {/* Duplicate Charges (Red) */}
                            {bill.analysis?.duplicateCharges?.length > 0 && (
                              <div className="rounded-lg border border-red-100 bg-red-50 p-3">
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
                                    (charge, idx) => (
                                      <div
                                        key={idx}
                                        className="rounded-md bg-white p-3 shadow-sm"
                                      >
                                        <p className="font-medium text-gray-900">
                                          {charge.description}
                                        </p>
                                        <div className="mt-1 flex items-center justify-between text-sm">
                                          <span className="text-red-600">
                                            Charged Twice
                                          </span>
                                          <span className="font-medium text-red-600">
                                            $
                                            {charge.originalAmount.toLocaleString()}
                                          </span>
                                        </div>
                                      </div>
                                    )
                                  )}
                                </div>
                              </div>
                            )}

                            {/* Overcharges (Amber) */}
                            {bill.analysis?.overcharges?.length > 0 && (
                              <div className="rounded-lg border border-amber-100 bg-amber-50 p-3">
                                <h5 className="flex items-center text-sm font-medium text-amber-800">
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
                                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                                    />
                                  </svg>
                                  Above Market Rate
                                </h5>
                                <div className="mt-3 space-y-2">
                                  {bill.analysis.overcharges.map(
                                    (charge, idx) => (
                                      <div
                                        key={idx}
                                        className="rounded-md bg-white p-3 shadow-sm"
                                      >
                                        <p className="font-medium text-gray-900">
                                          {charge.description}
                                        </p>
                                        <div className="mt-1 flex items-center justify-between text-sm">
                                          <span className="text-amber-600">
                                            Market Rate: $
                                            {charge.marketRate.toLocaleString()}
                                          </span>
                                          <span className="font-medium text-amber-600">
                                            Charged: $
                                            {charge.originalAmount.toLocaleString()}
                                          </span>
                                        </div>
                                      </div>
                                    )
                                  )}
                                </div>
                              </div>
                            )}

                            {/* Additional Savings (Blue) */}
                            {bill.analysis?.negotiableItems?.length > 0 && (
                              <div className="rounded-lg border border-blue-100 bg-blue-50 p-3">
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
                                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                                    />
                                  </svg>
                                  Additional Savings
                                </h5>
                                <div className="mt-3 space-y-2">
                                  {bill.analysis.negotiableItems.map(
                                    (item, idx) => (
                                      <div
                                        key={idx}
                                        className="rounded-md bg-white p-3 shadow-sm"
                                      >
                                        <p className="font-medium text-gray-900">
                                          {item.description}
                                        </p>
                                        <div className="mt-1 flex items-center justify-between text-sm">
                                          <span className="text-blue-600">
                                            Recommended: $
                                            {item.recommendedAmount.toLocaleString()}
                                          </span>
                                          <span className="font-medium text-blue-600">
                                            Current: $
                                            {item.originalAmount.toLocaleString()}
                                          </span>
                                        </div>
                                      </div>
                                    )
                                  )}
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Desktop View - Existing table structure */}
            <div className="hidden sm:block overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                      Bill Details
                    </th>
                    <th className="hidden sm:table-cell px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                      Date
                    </th>
                    <th className="hidden sm:table-cell px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                      Amount
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                      Potential Savings
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {importedBills.map((bill) => (
                    <Fragment key={bill.id}>
                      <tr
                        className="cursor-pointer hover:bg-gray-50"
                        onClick={() => toggleBillExpansion(bill.id)}
                      >
                        <td className="whitespace-nowrap px-6 py-4">
                          <div className="flex items-center">
                            <svg
                              className={`h-5 w-5 text-gray-400 transition-transform ${
                                expandedBills.includes(bill.id)
                                  ? "rotate-180"
                                  : ""
                              }`}
                              fill="none"
                              viewBox="0 0 24 24"
                              stroke="currentColor"
                            >
                              <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M19 9l-7 7-7-7"
                              />
                            </svg>
                            <span className="ml-4">{bill.description}</span>
                          </div>
                        </td>
                        <td className="hidden sm:table-cell whitespace-nowrap px-6 py-4">
                          <div className="text-sm text-gray-900">
                            {new Date(bill.date).toLocaleDateString("en-US", {
                              month: "short",
                              day: "numeric",
                              year: "numeric",
                            })}
                          </div>
                        </td>
                        <td className="hidden sm:table-cell whitespace-nowrap px-6 py-4">
                          <div className="text-sm text-gray-900">
                            ${bill.amount.toLocaleString()}
                          </div>
                        </td>
                        <td className="whitespace-nowrap px-6 py-4">
                          <span
                            className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                              bill.status === "Negotiating"
                                ? "bg-yellow-100 text-yellow-800"
                                : bill.status === "Analyzed"
                                  ? "bg-blue-100 text-blue-800"
                                  : bill.status === "Completed"
                                    ? "bg-green-100 text-green-800"
                                    : "bg-gray-100 text-gray-800"
                            }`}
                          >
                            {bill.status}
                          </span>
                        </td>
                        <td className="whitespace-nowrap px-6 py-4">
                          {bill.analysis?.totalPotentialSavings ? (
                            <div className="text-sm font-medium text-green-600">
                              $
                              {bill.analysis.totalPotentialSavings.toLocaleString()}
                            </div>
                          ) : (
                            <span className="text-sm text-gray-500">—</span>
                          )}
                        </td>
                        <td className="whitespace-nowrap px-6 py-4">
                          {bill.status === "Imported" && (
                            <button
                              onClick={() => analyzeBill(bill.id)}
                              className="text-sm font-medium text-blue-600 hover:text-blue-500"
                            >
                              {analyzingBills.includes(bill.id) ? (
                                <div className="flex items-center space-x-2">
                                  <svg
                                    className="h-4 w-4 animate-spin"
                                    viewBox="0 0 24 24"
                                  >
                                    <circle
                                      className="opacity-25"
                                      cx="12"
                                      cy="12"
                                      r="10"
                                      stroke="currentColor"
                                      strokeWidth="4"
                                      fill="none"
                                    />
                                    <path
                                      className="opacity-75"
                                      fill="currentColor"
                                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                    />
                                  </svg>
                                  <span>Analyzing...</span>
                                </div>
                              ) : (
                                "Analyze Bill"
                              )}
                            </button>
                          )}
                          {bill.status === "Analyzed" && (
                            <button
                              onClick={() => startNegotiation(bill.id)}
                              className="text-sm font-medium text-blue-600 hover:text-blue-500"
                            >
                              Start Negotiation
                            </button>
                          )}
                        </td>
                      </tr>
                      {/* Expanded Details Row */}
                      {expandedBills.includes(bill.id) && (
                        <tr>
                          <td colSpan={6} className="p-0">
                            <div className="bg-gray-50 p-4">
                              {/* Bill Summary Section */}
                              <div className="mb-6 rounded-lg border border-gray-200 bg-white p-4">
                                <div className="flex flex-col space-y-4 sm:flex-row sm:items-center sm:justify-between sm:space-y-0">
                                  <div>
                                    <h4 className="text-lg font-medium text-gray-900">
                                      {bill.description}
                                    </h4>
                                    <span className="mt-1 block text-sm text-gray-500 sm:mt-0 sm:ml-2 sm:inline">
                                      Original Amount: $
                                      {bill.amount.toLocaleString()}
                                    </span>
                                  </div>
                                  <div className="text-left sm:text-right">
                                    <div className="text-sm font-medium text-gray-500">
                                      Potential Savings
                                    </div>
                                    <div className="text-2xl font-bold text-green-600">
                                      $
                                      {bill.analysis?.totalPotentialSavings.toLocaleString()}
                                    </div>
                                  </div>
                                </div>

                                {/* Services and Details Grid */}
                                <div className="mt-4 grid gap-6 border-t border-gray-100 pt-4 sm:grid-cols-2">
                                  <div>
                                    <h5 className="text-sm font-medium text-gray-700">
                                      Services Provided
                                    </h5>
                                    <ul className="mt-2 space-y-1">
                                      {bill.analysis?.duplicateCharges?.map(
                                        (charge) => (
                                          <li
                                            key={charge.description}
                                            className="text-sm text-gray-600"
                                          >
                                            • {charge.description} - $
                                            {charge.originalAmount.toLocaleString()}
                                          </li>
                                        )
                                      )}
                                      {bill.analysis?.overcharges?.map(
                                        (charge) => (
                                          <li
                                            key={charge.description}
                                            className="text-sm text-gray-600"
                                          >
                                            • {charge.description} - $
                                            {charge.originalAmount.toLocaleString()}
                                          </li>
                                        )
                                      )}
                                      {bill.analysis?.negotiableItems?.map(
                                        (item) => (
                                          <li
                                            key={item.description}
                                            className="text-sm text-gray-600"
                                          >
                                            • {item.description} - $
                                            {item.originalAmount.toLocaleString()}
                                          </li>
                                        )
                                      )}
                                    </ul>
                                  </div>
                                  <div>
                                    <h5 className="text-sm font-medium text-gray-700">
                                      Bill Details
                                    </h5>
                                    <div className="mt-2 space-y-1 text-sm text-gray-600">
                                      <div>
                                        Date of Service:{" "}
                                        {new Date(bill.date).toLocaleDateString(
                                          "en-US",
                                          {
                                            month: "short",
                                            day: "numeric",
                                            year: "numeric",
                                          }
                                        )}
                                      </div>
                                      <div>Bill Type: {bill.type}</div>
                                      <div>Provider: {bill.provider}</div>
                                      <div>Status: {bill.status}</div>
                                    </div>
                                  </div>
                                </div>

                                {/* Move Negotiation Opportunities here */}
                                <div className="mt-6 border-t border-gray-100 pt-6">
                                  <h4 className="mb-4 text-lg font-medium text-gray-900">
                                    Negotiation Opportunities
                                  </h4>
                                  <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                                    {/* Duplicate Charges (Red) */}
                                    {bill.analysis?.duplicateCharges?.length >
                                      0 && (
                                      <div className="rounded-lg border border-red-100 bg-red-50 p-3">
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
                                            (charge, idx) => (
                                              <div
                                                key={idx}
                                                className="rounded-md bg-white p-3 shadow-sm"
                                              >
                                                <p className="font-medium text-gray-900">
                                                  {charge.description}
                                                </p>
                                                <div className="mt-1 flex items-center justify-between text-sm">
                                                  <span className="text-red-600">
                                                    Charged Twice
                                                  </span>
                                                  <span className="font-medium text-red-600">
                                                    $
                                                    {charge.originalAmount.toLocaleString()}
                                                  </span>
                                                </div>
                                              </div>
                                            )
                                          )}
                                        </div>
                                      </div>
                                    )}

                                    {/* Overcharges (Amber) */}
                                    {bill.analysis?.overcharges?.length > 0 && (
                                      <div className="rounded-lg border border-amber-100 bg-amber-50 p-3">
                                        <h5 className="flex items-center text-sm font-medium text-amber-800">
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
                                              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                                            />
                                          </svg>
                                          Above Market Rate
                                        </h5>
                                        <div className="mt-3 space-y-2">
                                          {bill.analysis.overcharges.map(
                                            (charge, idx) => (
                                              <div
                                                key={idx}
                                                className="rounded-md bg-white p-3 shadow-sm"
                                              >
                                                <p className="font-medium text-gray-900">
                                                  {charge.description}
                                                </p>
                                                <div className="mt-1 flex items-center justify-between text-sm">
                                                  <span className="text-amber-600">
                                                    Market Rate: $
                                                    {charge.marketRate.toLocaleString()}
                                                  </span>
                                                  <span className="font-medium text-amber-600">
                                                    Charged: $
                                                    {charge.originalAmount.toLocaleString()}
                                                  </span>
                                                </div>
                                              </div>
                                            )
                                          )}
                                        </div>
                                      </div>
                                    )}

                                    {/* Additional Savings (Blue) */}
                                    {bill.analysis?.negotiableItems?.length >
                                      0 && (
                                      <div className="rounded-lg border border-blue-100 bg-blue-50 p-3">
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
                                              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                                            />
                                          </svg>
                                          Additional Savings
                                        </h5>
                                        <div className="mt-3 space-y-2">
                                          {bill.analysis.negotiableItems.map(
                                            (item, idx) => (
                                              <div
                                                key={idx}
                                                className="rounded-md bg-white p-3 shadow-sm"
                                              >
                                                <p className="font-medium text-gray-900">
                                                  {item.description}
                                                </p>
                                                <div className="mt-1 flex items-center justify-between text-sm">
                                                  <span className="text-blue-600">
                                                    Recommended: $
                                                    {item.recommendedAmount.toLocaleString()}
                                                  </span>
                                                  <span className="font-medium text-blue-600">
                                                    Current: $
                                                    {item.originalAmount.toLocaleString()}
                                                  </span>
                                                </div>
                                              </div>
                                            )
                                          )}
                                        </div>
                                      </div>
                                    )}
                                  </div>
                                </div>
                              </div>
                            </div>
                          </td>
                        </tr>
                      )}
                    </Fragment>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
