export const testBills = {
    anthem: [
        {
            id: "anthem-eob-1",
            type: "EOB",
            provider: "anthem",
            date: "2024-02-15",
            amount: 1250.00,
            description: "Emergency Room Visit",
            fileName: "anthem-eob-example-1.pdf",
            thumbnail: "/images/bills/eob-example.png"
        },
        {
            id: "anthem-bill-1",
            type: "Bill",
            provider: "anthem",
            date: "2024-02-15",
            amount: 350.00,
            description: "Lab Services",
            fileName: "anthem-bill-example-1.pdf",
            thumbnail: "/images/bills/bill-example.png"
        },
        {
            id: "anthem-eob-2",
            type: "EOB",
            provider: "anthem",
            date: "2024-01-20",
            amount: 2100.00,
            description: "Outpatient Surgery",
            fileName: "anthem-eob-example-2.pdf",
            thumbnail: "/images/bills/eob-example-2.png"
        }
    ],
    uhc: [
        {
            id: "uhc-eob-1",
            type: "EOB",
            provider: "uhc",
            date: "2024-02-01",
            amount: 1800.00,
            description: "MRI Scan",
            fileName: "uhc-eob-example-1.pdf",
            thumbnail: "/images/bills/eob-example-3.png"
        },
        {
            id: "uhc-bill-1",
            type: "Bill",
            provider: "uhc",
            date: "2024-02-01",
            amount: 450.00,
            description: "Specialist Consultation",
            fileName: "uhc-bill-example-1.pdf",
            thumbnail: "/images/bills/bill-example-2.png"
        }
    ],
    // Add more providers...
} 