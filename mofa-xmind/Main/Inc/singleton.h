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

#if !defined(FORCE_INLINE)
#if defined(_MSC_VER)
// Microsoft Visual C++ Compiler
#define FORCE_INLINE __forceinline
#elif defined(BARE_METAL)
#define FORCE_INLINE inline
#elif defined(__GNUC__) || defined(__clang__)
// GCC or Clang Compiler
#define FORCE_INLINE __attribute__((always_inline)) inline
#else
// Fallback for other compilers
#define FORCE_INLINE inline
#endif
#endif

template <class T> 
class Singleton { 
public: 
	FORCE_INLINE static T& I() { 
		static T _instance; 
		return _instance; 
	} 

protected: 
	Singleton(void) {} 
	virtual ~Singleton(void) {} 
	Singleton(const Singleton<T>&); 
	Singleton<T>& operator= (const Singleton<T> &); 
}; 