# Import AsyncIO

This is a learning exercise where I followed [ambv](github.com/ambv)'s tutorial on the asyncio and its internals.

The vide can he found [here](https://www.youtube.com/watch?v=SyiTd4rLb2s)

## Coroutine Synchronization

From time [56:40](https://youtu.be/SyiTd4rLb2s?t=3400)

Note: Synchronization Primitives are hard and can lead to race conditions

It's a tricky subject and there are plenty of options to shoot yourself on the foot.

### 1. Lock

> class asyncio.Lock(*, loop=None)

```
Once a coroutine acquires a lock subsequent attempts to acquire it will wait untill the first one releases it.

Lock is async context managers all the way down
```

```python
lock = asyncio.Lock()

async with lock:
```

### 2. Event

> class asyncio.Event(*, loop=None)

```
Probably the simplest form of communication between coroutines.

One coroutine signals an event and other coroutines wait for it. Essently a single flag you can use in your program
```

```python
async def waiter(event):
    print('waiting for it...')
    await event.wait()
    print('... got it!')

async def main():
    # create an Event object
    event = asyncio.Event()

    # spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.create_task(waiter(event))

    # sleep for 1 sec and set the event
    await asyncio.sleep(1)
    event.set()

    # wait until the waiter task is finished.
    await waiter_task

asyncio.run(main())
```
### 3. Semaphore

> class asyncio.Semaphore(value=1, *, loop=None)

```
Semaphores are like locks, but they allow more than a single coroutine to acquire it at a time. It allows to control load on a restricted or controlled source.

When dealing with Semaphores you decide a concurrency level.
```

```python
sem = asyncio.Semaphore(10)

# ... later
async with sem:
    # work with shared resource
```
### 4. Condition

> class asyncio.Condition(lock=None, *, loop=None)

```
The most complex and not used that often.

It is used when Queues are insufficient. Like an Event, you have two sides for the system - a producer and consumer. The producer acquires the Condition object, produces some item and notifies one or more consumers using notifiy or notifiy_all method.

On the consumer side, it acquires the notification object and awaits on a notification, using the wait coroutine - simialer to events. So you wait on the Condition and in consequence the producer calls notify and the consmer's wait is done

Why use it?

When there is a shared resource that requires a lock to acess, but the lock is insufficient to determine if the shared resource is in a usable state.
```

```python
cond = asyncio.Condition()

# ... later
async with cond:
    await cond.wait()
```
