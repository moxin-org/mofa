/*
Copyright (C) 2024 The XLang Foundation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#pragma once

typedef void* PasWaitHandle;

#if (WIN32)
#define Path_Sep_S "\\"
#define Path_Sep '\\'
#define SCANF sscanf_s
#define SPRINTF sprintf_s
#define STRCMPNOCASE _strnicmp
#define MS_SLEEP(t) Sleep(t)
#define US_SLEEP(t) Sleep(t/1000)
#else
#define Path_Sep_S "/"
#define Path_Sep '/'
#include <strings.h>
#include <memory.h>
#include <netinet/in.h>
#define SCANF sscanf
#define SPRINTF snprintf

#define STRCMPNOCASE strncasecmp
#define MS_SLEEP(t)  usleep((t)*1000)
#define US_SLEEP(t) usleep(t)
#endif


#if (WIN32)
#include <windows.h>
#define SEMAPHORE_HANDLE HANDLE
#define CREATE_SEMAPHORE(sa,name) CreateEvent(&sa, FALSE,FALSE, name)
#define OPEN_SEMAPHORE(name) OpenEvent(EVENT_ALL_ACCESS, FALSE, name)
#define WAIT_FOR_SEMAPHORE(handle, timeout) WaitForSingleObject(handle, timeout)
#define CLOSE_SEMAPHORE(handle) CloseHandle(handle)
#else
#include <fcntl.h>
#include <semaphore.h>
#include <sys/stat.h>
#define SEMAPHORE_HANDLE sem_t*
#define CREATE_SEMAPHORE(sa,name) sem_open(name, O_CREAT | O_EXCL, 0644, 1)
#define OPEN_SEMAPHORE(name) sem_open(name, 0)
#define WAIT_FOR_SEMAPHORE(handle, timeout) sem_wait(handle) // Implement timeout if needed
#define CLOSE_SEMAPHORE(handle) sem_close(handle)
#endif
