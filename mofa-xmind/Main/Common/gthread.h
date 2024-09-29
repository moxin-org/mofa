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

#ifndef __gthread_h__
#define __gthread_h__


class GThread
{
public:
    GThread()
    {

    }
    virtual ~GThread()
    {

    }
    virtual bool Start();
    virtual void Stop();
    virtual void WaitToEnd();
public:
    virtual void run() =0;
protected:
    void* mThreadHandle =nullptr;
};

class GThread2
    :public virtual GThread
{
public:
    virtual bool Start();
    virtual void Stop();
    virtual void WaitToEnd();
    virtual void run2() = 0;
protected:
    void* mThreadHandle2 = nullptr;
};

class GThread3
    :public virtual GThread2
{
public:
    virtual bool Start();
    virtual void Stop();
    virtual void WaitToEnd();
    virtual void run3() = 0;
protected:
    void* mThreadHandle3 = nullptr;
};

#endif //!__gthread_h__