#include <windows.h>
//#include <wdm.h>
#include <iostream>
#include <fstream>
#include <chrono>

// Variáveis para rastrear o número de chamadas e o tempo da última chamada
static int callCount = 0;
static std::chrono::time_point<std::chrono::steady_clock> lastCallTime;

// Constante para o limite de chamadas por segundo
const int CALL_LIMIT = 5;

// Função auxiliar para verificar se atingiu o limite de chamadas em 1 segundo
bool IsCallLimitExceeded() {
    auto currentTime = std::chrono::steady_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(currentTime - lastCallTime);
    return (elapsed.count() < 1) && (callCount >= CALL_LIMIT);
}

// Definindo os tipos
typedef VOID(NTAPI* PIO_APC_ROUTINE) (
    IN PVOID ApcContext,
    IN PVOID IoStatusBlock,
    IN ULONG Reserved
    );

// Obtendo um ponteiro para a função NtClose
typedef NTSTATUS(NTAPI* NtClose_t)(HANDLE);
NtClose_t NtClose = (NtClose_t)GetProcAddress(GetModuleHandleW(L"ntdll"), "NtClose");

extern "C" __declspec(dllexport) NTSTATUS new_write(
    HANDLE           FileHandle,
    HANDLE           Event,
    PIO_APC_ROUTINE  ApcRoutine,
    PVOID            ApcContext,
    PVOID IoStatusBlock,
    PVOID            Buffer,
    ULONG            Length,
    PLARGE_INTEGER   ByteOffset,
    PULONG           Key
) {
    // Verificar se o limite de chamadas foi excedido
    if (IsCallLimitExceeded()) {

        // Chame a função NtClose em vez de NtWriteFile
        return NtClose(FileHandle);
    }

    // Se o limite de chamadas não foi excedido, registre a chamada e a hora atual
    callCount++;
    lastCallTime = std::chrono::steady_clock::now();

    // Obter o ID do processo que chamou esta função
    DWORD processId = GetCurrentProcessId();

    // Abrir o processo
    HANDLE hProcess = OpenProcess(PROCESS_TERMINATE, FALSE, processId);

    if (hProcess != nullptr)
    {
        // Terminar o processo
        TerminateProcess(hProcess, 0);

        // Fechar o handle do processo
        CloseHandle(hProcess);
    }

    // Chame a função NtClose em vez de NtWriteFile
    return NtClose(FileHandle);
}
