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
  };
};

type ConnectedProvider = {
  id: string;
  name: string;
  logo: string;
  connectedAt: string;
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
          const totalAmount = bill.amount;
          const targetSavings = totalAmount * 0.3;

          return {
            ...bill,
            status: "Analyzed" as const,
            analysis: {
              duplicateCharges: [
                {
                  description: "Lab Test - Complete Blood Count",
                  originalAmount: Math.round(totalAmount * 0.15),
                  duplicateAmount: Math.round(totalAmount * 0.15),
                  potential_saving: Math.round(totalAmount * 0.15),
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
              totalPotentialSavings: Math.round(targetSavings),
            },
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
          <div className="flex items-center justify-between rounded-lg bg-white p-6 shadow-sm ring-1 ring-gray-100">
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
                  {new Date(connectedProvider.connectedAt).toLocaleDateString()}
                </p>
              </div>
            </div>
            <Link
              href="/welcome"
              onClick={() => {
                // Set current step to 2 in localStorage
                const currentSteps = JSON.parse(
                  localStorage.getItem("completedSteps") || "[]"
                );
                localStorage.setItem(
                  "completedSteps",
                  JSON.stringify(Array.from(new Set([...currentSteps, 1])))
                );
              }}
              className="inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
            >
              Import More Bills
            </Link>
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
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    Bill Details
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
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
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-medium text-gray-900">
                              {bill.description}
                            </div>
                            <div className="mt-1 flex items-center space-x-2">
                              <span className="text-sm text-gray-500">
                                {new Date(bill.date).toLocaleDateString()}
                              </span>
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
                          </div>
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
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-6 py-4">
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
                        <td colSpan={5} className="bg-gray-50 px-6 py-4">
                          {/* Bill Summary Section */}
                          <div className="mb-6 rounded-lg border border-gray-200 bg-white p-4">
                            <div className="flex items-center justify-between">
                              <div>
                                <h4 className="text-lg font-medium text-gray-900">
                                  {bill.description}
                                  <span className="ml-2 text-sm text-gray-500">
                                    Original Amount: $
                                    {bill.amount.toLocaleString()}
                                  </span>
                                </h4>
                              </div>
                              <div className="text-right">
                                <div className="text-sm font-medium text-gray-500">
                                  Potential Savings
                                </div>
                                <div className="text-2xl font-bold text-green-600">
                                  $
                                  {bill.analysis?.totalPotentialSavings.toLocaleString()}
                                </div>
                              </div>
                            </div>
                            <div className="mt-4 grid gap-4 border-t border-gray-100 pt-4 md:grid-cols-2">
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
                                    {new Date(bill.date).toLocaleDateString()}
                                  </div>
                                  <div>Bill Type: {bill.type}</div>
                                  <div>Provider: {bill.provider}</div>
                                  <div>Status: {bill.status}</div>
                                </div>
                              </div>
                            </div>
                          </div>

                          {/* Savings Analysis Grid */}
                          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                            {/* Duplicate Charges */}
                            {bill.analysis &&
                              bill.analysis.duplicateCharges &&
                              bill.analysis.duplicateCharges.length > 0 && (
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

                            {/* Above Market Rate */}
                            {bill.analysis &&
                              bill.analysis.overcharges &&
                              bill.analysis.overcharges.length > 0 && (
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
                                      (charge, idx) => (
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
                                                $
                                                {charge.originalAmount.toLocaleString()}
                                              </span>
                                            </div>
                                            <div className="flex justify-between">
                                              <span className="text-green-600">
                                                Market Rate
                                              </span>
                                              <span className="font-medium text-green-600">
                                                $
                                                {charge.marketRate.toLocaleString()}
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
                            {bill.analysis &&
                              bill.analysis.negotiableItems &&
                              bill.analysis.negotiableItems.length > 0 && (
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
                                      (item, idx) => (
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
                                                $
                                                {item.originalAmount.toLocaleString()}
                                              </span>
                                            </div>
                                            <div className="flex justify-between">
                                              <span className="text-blue-600">
                                                Target Amount
                                              </span>
                                              <span className="font-medium text-blue-600">
                                                $
                                                {item.recommendedAmount.toLocaleString()}
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
  );
}
