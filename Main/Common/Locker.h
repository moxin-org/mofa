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

#ifndef Locker_H
#define Locker_H

#ifdef WIN32
#include <Windows.h>
#else
#include <mutex> 
#endif
class Locker
{
public:
	Locker();
	~Locker();

	inline void Lock()
	{
#ifndef WIN32
		m_cs.lock();
#else
		::EnterCriticalSection(&m_cs);
#endif
	}

	inline void Unlock()
	{
#ifndef WIN32
		m_cs.unlock();
#else
		::LeaveCriticalSection(&m_cs);
#endif
	}

private:
#ifndef WIN32
	std::recursive_mutex m_cs;
#else
	CRITICAL_SECTION m_cs;
#endif
};

class AutoLock
{
public:
	AutoLock() :
		m_lock(NULL)
	{
	}

	AutoLock(Locker& lk)
	{
		m_lock = &lk;
		lk.Lock();
	}

	~AutoLock()
	{
		if (m_lock)
		{
			m_lock->Unlock();
		}
	}

private:
	Locker* m_lock;
};

#endif //Locker_H
