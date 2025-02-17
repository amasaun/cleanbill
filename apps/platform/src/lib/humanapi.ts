export const connectInsuranceProvider = async (clientId: string, userId: string) => {
    const connectToken = await getConnectToken() // Get from your backend

    const options = {
        clientId,
        clientUserId: userId,
        connectToken,
        language: "en",
        mode: "insurance",
        onClose: () => {
            // Handle close
        },
        onConnect: (data: any) => {
            // Handle successful connection
        },
        onError: (error: any) => {
            // Handle error
        }
    }

    // @ts-ignore - Human API types
    window.HumanConnect.open(options)
} 