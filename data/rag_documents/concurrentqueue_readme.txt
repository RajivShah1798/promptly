# Samples for moodycamel::ConcurrentQueue

Here are some example usage scenarios with sample code. Note that most
use the simplest version of each available method for demonstration purposes,
but they can all be adapted to use tokens and/or the corresponding bulk methods for
extra speed.


## Hello queue
```C++
ConcurrentQueue<int> q;

for (int i = 0; i != 123; ++i)
	q.enqueue(i);

int item;
for (int i = 0; i != 123; ++i) {
	q.try_dequeue(item);
	assert(item == i);
}
```

## Hello concurrency

Basic example of how to use the queue from multiple threads, with no
particular goal (i.e. it does nothing, but in an instructive way).
```C++
ConcurrentQueue<int> q;
int dequeued[100] = { 0 };
std::thread threads[20];

// Producers
for (int i = 0; i != 10; ++i) {
	threads[i] = std::thread([&](int i) {
		for (int j = 0; j != 10; ++j) {
			q.enqueue(i * 10 + j);
		}
	}, i);
}

// Consumers
for (int i = 10; i != 20; ++i) {
	threads[i] = std::thread([&]() {
		int item;
		for (int j = 0; j != 20; ++j) {
			if (q.try_dequeue(item)) {
				++dequeued[item];
			}
		}
	});
}

// Wait for all threads
for (int i = 0; i != 20; ++i) {
	threads[i].join();
}

// Collect any leftovers (could be some if e.g. consumers finish before producers)
int item;
while (q.try_dequeue(item)) {
	++dequeued[item];
}

// Make sure everything went in and came back out!
for (int i = 0; i != 100; ++i) {
	assert(dequeued[i] == 1);
}
```

## Bulk up

Same as previous example, but runs faster.
```C++
ConcurrentQueue<int> q;
int dequeued[100] = { 0 };
std::thread threads[20];

// Producers
for (int i = 0; i != 10; ++i) {
	threads[i] = std::thread([&](int i) {
		int items[10];
		for (int j = 0; j != 10; ++j) {
			items[j] = i * 10 + j;
		}
		q.enqueue_bulk(items, 10);
	}, i);
}

// Consumers
for (int i = 10; i != 20; ++i) {
	threads[i] = std::thread([&]() {
		int items[20];
		for (std::size_t count = q.try_dequeue_bulk(items, 20); count != 0; --count) {
			++dequeued[items[count - 1]];
		}
	});
}

// Wait for all threads
for (int i = 0; i != 20; ++i) {
	threads[i].join();
}

// Collect any leftovers (could be some if e.g. consumers finish before producers)
int items[10];
std::size_t count;
while ((count = q.try_dequeue_bulk(items, 10)) != 0) {
	for (std::size_t i = 0; i != count; ++i) {
		++dequeued[items[i]];
	}
}

// Make sure everything went in and came back out!
for (int i = 0; i != 100; ++i) {
	assert(dequeued[i] == 1);
}
```

## Producer/consumer model (simultaneous)

In this model, one set of threads is producing items,
and the other is consuming them concurrently until all of
them have been consumed. The counters are required to
ensure that all items eventually get consumed.
```C++
ConcurrentQueue<Item> q;
const int ProducerCount = 8;
const int ConsumerCount = 8;
std::thread producers[ProducerCount];
std::thread consumers[ConsumerCount];
std::atomic<int> doneProducers(0);
std::atomic<int> doneConsumers(0);
for (int i = 0; i != ProducerCount; ++i) {
	producers[i] = std::thread([&]() {
		while (produce) {
			q.enqueue(produceItem());
		}
		doneProducers.fetch_add(1, std::memory_order_release);
	});
}
for (int i = 0; i != ConsumerCount; ++i) {
	consumers[i] = std::thread([&]() {
		Item item;
		bool itemsLeft;
		do {
			// It's important to fence (if the producers have finished) *before* dequeueing
			itemsLeft = doneProducers.load(std::memory_order_acquire) != ProducerCount;
			while (q.try_dequeue(item)) {
				itemsLeft = true;
				consumeItem(item);
			}
		} while (itemsLeft || doneConsumers.fetch_add(1, std::memory_order_acq_rel) + 1 == ConsumerCount);
		// The condition above is a bit tricky, but it's necessary to ensure that the
		// last consumer sees the memory effects of all the other consumers before it
		// calls try_dequeue for the last time
	});
}
for (int i = 0; i != ProducerCount; ++i) {
	producers[i].join();
}
for (int i = 0; i != ConsumerCount; ++i) {
	consumers[i].join();
}
```
## Producer/consumer model (simultaneous, blocking)

The blocking version is different, since either the number of elements being produced needs
to be known ahead of time, or some other coordination is required to tell the consumers when
to stop calling wait_dequeue (not shown here). This is necessary because otherwise a consumer
could end up blocking forever -- and destroying a queue while a consumer is blocking on it leads
to undefined behaviour.
```C++
BlockingConcurrentQueue<Item> q;
const int ProducerCount = 8;
const int ConsumerCount = 8;
std::thread producers[ProducerCount];
std::thread consumers[ConsumerCount];
std::atomic<int> promisedElementsRemaining(ProducerCount * 1000);
for (int i = 0; i != ProducerCount; ++i) {
	producers[i] = std::thread([&]() {
		for (int j = 0; j != 1000; ++j) {
			q.enqueue(produceItem());
		}
	});
}
for (int i = 0; i != ConsumerCount; ++i) {
	consumers[i] = std::thread([&]() {
		Item item;
		while (promisedElementsRemaining.fetch_sub(1, std::memory_order_relaxed)) {
			q.wait_dequeue(item);
			consumeItem(item);
		}
	});
}
for (int i = 0; i != ProducerCount; ++i) {
	producers[i].join();
}
for (int i = 0; i != ConsumerCount; ++i) {
	consumers[i].join();
}
```

## Producer/consumer model (separate stages)
```C++
ConcurrentQueue<Item> q;

// Production stage
std::thread threads[8];
for (int i = 0; i != 8; ++i) {
	threads[i] = std::thread([&]() {
		while (produce) {
			q.enqueue(produceItem());
		}
	});
}
for (int i = 0; i != 8; ++i) {
	threads[i].join();
}

// Consumption stage
std::atomic<int> doneConsumers(0);
for (int i = 0; i != 8; ++i) {
	threads[i] = std::thread([&]() {
		Item item;
		do {
			while (q.try_dequeue(item)) {
				consumeItem(item);
			}
			// Loop again one last time if we're the last producer (with the acquired
			// memory effects of the other producers):
		} while (doneConsumers.fetch_add(1, std::memory_order_acq_rel) + 1 == 8);
	});
}
for (int i = 0; i != 8; ++i) {
	threads[i].join();
}
```
Note that there's no point trying to use the blocking queue with this model, since
there's no need to use the `wait` methods (all the elements are produced before any
are consumed), and hence the complexity would be the same but with additional overhead.


## Object pool

If you don't know what threads will be using the queue in advance,
you can't really declare any long-term tokens. The obvious solution
is to use the implicit methods (that don't take any tokens):
```C++
// A pool of 'Something' objects that can be safely accessed
// from any thread
class SomethingPool
{
public:
    Something getSomething()
    {
	Something obj;
	queue.try_dequeue(obj);

	// If the dequeue succeeded, obj will be an object from the
	// thread pool, otherwise it will be the default-constructed
	// object as declared above
	return obj;
    }

    void recycleSomething(Something&& obj)
    {
	queue.enqueue(std::move(obj));
    }
};
```

## Threadpool task queue
```C++
BlockingConcurrentQueue<Task> q;

// To create a task from any thread:
q.enqueue(...);

// On threadpool threads:
Task task;
while (true) {
	q.wait_dequeue(task);

	// Process task...
}
```

## Multithreaded game loop
```C++
BlockingConcurrentQueue<Task> q;
std::atomic<int> pendingTasks(0);

// On threadpool threads:
Task task;
while (true) {
	q.wait_dequeue(task);

	// Process task...

	pendingTasks.fetch_add(-1, std::memory_order_release);
}

// Whenever a new task needs to be processed for the frame:
pendingTasks.fetch_add(1, std::memory_order_release);
q.enqueue(...);

// To wait for all the frame's tasks to complete before rendering:
while (pendingTasks.load(std::memory_order_acquire) != 0)
	continue;

// Alternatively you could help out the thread pool while waiting:
while (pendingTasks.load(std::memory_order_acquire) != 0) {
	if (!q.try_dequeue(task)) {
		continue;
	}

	// Process task...

	pendingTasks.fetch_add(-1, std::memory_order_release);
}
```

## Pump until empty

This might be useful if, for example, you want to process any remaining items
in the queue before it's destroyed. Note that it is your responsibility
to ensure that the memory effects of any enqueue operations you wish to see on
the dequeue thread are visible (i.e. if you're waiting for a certain set of elements,
you need to use memory fences to ensure that those elements are visible to the dequeue
thread after they've been enqueued).
```C++
ConcurrentQueue<Item> q;

// Single-threaded pumping:
Item item;
while (q.try_dequeue(item)) {
	// Process item...
}
// q is guaranteed to be empty here, unless there is another thread enqueueing still or
// there was another thread dequeueing at one point and its memory effects have not
// yet been propagated to this thread.

// Multi-threaded pumping:
std::thread threads[8];
std::atomic<int> doneConsumers(0);
for (int i = 0; i != 8; ++i) {
	threads[i] = std::thread([&]() {
		Item item;
		do {
			while (q.try_dequeue(item)) {
				// Process item...
			}
		} while (doneConsumers.fetch_add(1, std::memory_order_acq_rel) + 1 == 8);
		// If there are still enqueue operations happening on other threads,
		// then the queue may not be empty at this point. However, if all enqueue
		// operations completed before we finished pumping (and the propagation of
		// their memory effects too), and all dequeue operations apart from those
		// our threads did above completed before we finished pumping (and the
		// propagation of their memory effects too), then the queue is guaranteed
		// to be empty at this point.
	});
}
for (int i = 0; i != 8; ++i) {
	threads[i].join();
}
```

## Wait for a queue to become empty (without dequeueing)

You can't (robustly) :-) However, you can set up your own atomic counter and
poll that instead (see the game loop example). If you're satisfied with merely an estimate, you can use
`size_approx()`. Note that `size_approx()` may return 0 even if the queue is
not completely empty, unless the queue has already stabilized first (no threads
are enqueueing or dequeueing, and all memory effects of any previous operations
have been propagated to the thread before it calls `size_approx()`).
# moodycamel::ConcurrentQueue<T>

An industrial-strength lock-free queue for C++.

Note: If all you need is a single-producer, single-consumer queue, I have [one of those too][spsc].

## Features

- Knock-your-socks-off [blazing fast performance][benchmarks].
- Single-header implementation. Just drop it in your project.
- Fully thread-safe lock-free queue. Use concurrently from any number of threads.
- C++11 implementation -- elements are moved (instead of copied) where possible.
- Templated, obviating the need to deal exclusively with pointers -- memory is managed for you.
- No artificial limitations on element types or maximum count.
- Memory can be allocated once up-front, or dynamically as needed.
- Fully portable (no assembly; all is done through standard C++11 primitives).
- Supports super-fast bulk operations.
- Includes a low-overhead blocking version (BlockingConcurrentQueue).
- Exception safe.

## Reasons to use

There are not that many full-fledged lock-free queues for C++. Boost has one, but it's limited to objects with trivial
assignment operators and trivial destructors, for example.
Intel's TBB queue isn't lock-free, and requires trivial constructors too.
There're many academic papers that implement lock-free queues in C++, but usable source code is
hard to find, and tests even more so.

This queue not only has less limitations than others (for the most part), but [it's also faster][benchmarks].
It's been fairly well-tested, and offers advanced features like **bulk enqueueing/dequeueing**
(which, with my new design, is much faster than one element at a time, approaching and even surpassing
the speed of a non-concurrent queue even under heavy contention).

In short, there was a lock-free queue shaped hole in the C++ open-source universe, and I set out
to fill it with the fastest, most complete, and well-tested design and implementation I could.
The result is `moodycamel::ConcurrentQueue` :-)

## Reasons *not* to use

The fastest synchronization of all is the kind that never takes place. Fundamentally,
concurrent data structures require some synchronization, and that takes time. Every effort
was made, of course, to minimize the overhead, but if you can avoid sharing data between
threads, do so!

Why use concurrent data structures at all, then? Because they're gosh darn convenient! (And, indeed,
sometimes sharing data concurrently is unavoidable.)

My queue is **not linearizable** (see the next section on high-level design). The foundations of
its design assume that producers are independent; if this is not the case, and your producers
co-ordinate amongst themselves in some fashion, be aware that the elements won't necessarily
come out of the queue in the same order they were put in *relative to the ordering formed by that co-ordination*
(but they will still come out in the order they were put in by any *individual* producer). If this affects
your use case, you may be better off with another implementation; either way, it's an important limitation
to be aware of.

My queue is also **not NUMA aware**, and does a lot of memory re-use internally, meaning it probably doesn't
scale particularly well on NUMA architectures; however, I don't know of any other lock-free queue that *is*
NUMA aware (except for [SALSA][salsa], which is very cool, but has no publicly available implementation that I know of).

Finally, the queue is **not sequentially consistent**; there *is* a happens-before relationship between when an element is put
in the queue and when it comes out, but other things (such as pumping the queue until it's empty) require more thought
to get right in all eventualities, because explicit memory ordering may have to be done to get the desired effect. In other words,
it can sometimes be difficult to use the queue correctly. This is why it's a good idea to follow the [samples][samples.md] where possible.
On the other hand, the upside of this lack of sequential consistency is better performance.

## High-level design

Elements are stored internally using contiguous blocks instead of linked lists for better performance.
The queue is made up of a collection of sub-queues, one for each producer. When a consumer
wants to dequeue an element, it checks all the sub-queues until it finds one that's not empty.
All of this is largely transparent to the user of the queue, however -- it mostly just works<sup>TM</sup>.

One particular consequence of this design, however, (which seems to be non-intuitive) is that if two producers
enqueue at the same time, there is no defined ordering between the elements when they're later dequeued.
Normally this is fine, because even with a fully linearizable queue there'd be a race between the producer
threads and so you couldn't rely on the ordering anyway. However, if for some reason you do extra explicit synchronization
between the two producer threads yourself, thus defining a total order between enqueue operations, you might expect
that the elements would come out in the same total order, which is a guarantee my queue does not offer. At that
point, though, there semantically aren't really two separate producers, but rather one that happens to be spread
across multiple threads. In this case, you can still establish a total ordering with my queue by creating
a single producer token, and using that from both threads to enqueue (taking care to synchronize access to the token,
of course, but there was already extra synchronization involved anyway).

I've written a more detailed [overview of the internal design][blog], as well as [the full
nitty-gritty details of the design][design], on my blog. Finally, the
[source][source] itself is available for perusal for those interested in its implementation.

## Basic use

The entire queue's implementation is contained in **one header**, [`concurrentqueue.h`][concurrentqueue.h].
Simply download and include that to use the queue. The blocking version is in a separate header,
[`blockingconcurrentqueue.h`][blockingconcurrentqueue.h], that depends on [`concurrentqueue.h`][concurrentqueue.h] and
[`lightweightsemaphore.h`][lightweightsemaphore.h]. The implementation makes use of certain key C++11 features,
so it requires a fairly recent compiler (e.g. VS2012+ or g++ 4.8; note that g++ 4.6 has a known bug with `std::atomic`
and is thus not supported). The algorithm implementations themselves are platform independent.

Use it like you would any other templated queue, with the exception that you can use
it from many threads at once :-)

Simple example:

    #include "concurrentqueue.h"
    
    moodycamel::ConcurrentQueue<int> q;
    q.enqueue(25);
    
    int item;
    bool found = q.try_dequeue(item);
    assert(found && item == 25);

Description of basic methods:
- `ConcurrentQueue(size_t initialSizeEstimate)`
      Constructor which optionally accepts an estimate of the number of elements the queue will hold
- `enqueue(T&& item)`
      Enqueues one item, allocating extra space if necessary
- `try_enqueue(T&& item)`
      Enqueues one item, but only if enough memory is already allocated
- `try_dequeue(T& item)`
      Dequeues one item, returning true if an item was found or false if the queue appeared empty

Note that it is up to the user to ensure that the queue object is completely constructed before
being used by any other threads (this includes making the memory effects of construction
visible, possibly via a memory barrier). Similarly, it's important that all threads have
finished using the queue (and the memory effects have fully propagated) before it is
destructed.

There's usually two versions of each method, one "explicit" version that takes a user-allocated per-producer or
per-consumer token, and one "implicit" version that works without tokens. Using the explicit methods is almost
always faster (though not necessarily by a huge factor). Apart from performance, the primary distinction between them
is their sub-queue allocation behaviour for enqueue operations: Using the implicit enqueue methods causes an
automatically-allocated thread-local producer sub-queue to be allocated (it is marked for reuse once the thread exits).
Explicit producers, on the other hand, are tied directly to their tokens' lifetimes (and are also recycled as needed).

Full API (pseudocode):

	# Allocates more memory if necessary
	enqueue(item) : bool
	enqueue(prod_token, item) : bool
	enqueue_bulk(item_first, count) : bool
	enqueue_bulk(prod_token, item_first, count) : bool
	
	# Fails if not enough memory to enqueue
	try_enqueue(item) : bool
	try_enqueue(prod_token, item) : bool
	try_enqueue_bulk(item_first, count) : bool
	try_enqueue_bulk(prod_token, item_first, count) : bool
	
	# Attempts to dequeue from the queue (never allocates)
	try_dequeue(item&) : bool
	try_dequeue(cons_token, item&) : bool
	try_dequeue_bulk(item_first, max) : size_t
	try_dequeue_bulk(cons_token, item_first, max) : size_t
	
	# If you happen to know which producer you want to dequeue from
	try_dequeue_from_producer(prod_token, item&) : bool
	try_dequeue_bulk_from_producer(prod_token, item_first, max) : size_t
	
	# A not-necessarily-accurate count of the total number of elements
	size_approx() : size_t

## Blocking version

As mentioned above, a full blocking wrapper of the queue is provided that adds
`wait_dequeue` and `wait_dequeue_bulk` methods in addition to the regular interface.
This wrapper is extremely low-overhead, but slightly less fast than the non-blocking
queue (due to the necessary bookkeeping involving a lightweight semaphore).

There are also timed versions that allow a timeout to be specified (either in microseconds
or with a `std::chrono` object).

The only major caveat with the blocking version is that you must be careful not to
destroy the queue while somebody is waiting on it. This generally means you need to
know for certain that another element is going to come along before you call one of
the blocking methods. (To be fair, the non-blocking version cannot be destroyed while
in use either, but it can be easier to coordinate the cleanup.)

Blocking example:

    #include "blockingconcurrentqueue.h"
    
    moodycamel::BlockingConcurrentQueue<int> q;
    std::thread producer([&]() {
        for (int i = 0; i != 100; ++i) {
            std::this_thread::sleep_for(std::chrono::milliseconds(i % 10));
            q.enqueue(i);
        }
    });
    std::thread consumer([&]() {
        for (int i = 0; i != 100; ++i) {
            int item;
            q.wait_dequeue(item);
            assert(item == i);
            
            if (q.wait_dequeue_timed(item, std::chrono::milliseconds(5))) {
                ++i;
                assert(item == i);
            }
        }
    });
    producer.join();
    consumer.join();
    
    assert(q.size_approx() == 0);

## Advanced features

#### Tokens

The queue can take advantage of extra per-producer and per-consumer storage if
it's available to speed up its operations. This takes the form of "tokens":
You can create a consumer token and/or a producer token for each thread or task
(tokens themselves are not thread-safe), and use the methods that accept a token
as their first parameter:

    moodycamel::ConcurrentQueue<int> q;
    
    moodycamel::ProducerToken ptok(q);
    q.enqueue(ptok, 17);
    
    moodycamel::ConsumerToken ctok(q);
    int item;
    q.try_dequeue(ctok, item);
    assert(item == 17);

If you happen to know which producer you want to consume from (e.g. in
a single-producer, multi-consumer scenario), you can use the `try_dequeue_from_producer`
methods, which accept a producer token instead of a consumer token, and cut some overhead.

Note that tokens work with the blocking version of the queue too.

When producing or consuming many elements, the most efficient way is to:

1. Use the bulk methods of the queue with tokens
2. Failing that, use the bulk methods without tokens
3. Failing that, use the single-item methods with tokens
4. Failing that, use the single-item methods without tokens

Having said that, don't create tokens willy-nilly -- ideally there would be
one token (of each kind) per thread. The queue will work with what it is
given, but it performs best when used with tokens.

Note that tokens aren't actually tied to any given thread; it's not technically
required that they be local to the thread, only that they be used by a single
producer/consumer at a time.

#### Bulk operations

Thanks to the [novel design][blog] of the queue, it's just as easy to enqueue/dequeue multiple
items as it is to do one at a time. This means that overhead can be cut drastically for
bulk operations. Example syntax:

    moodycamel::ConcurrentQueue<int> q;

    int items[] = { 1, 2, 3, 4, 5 };
    q.enqueue_bulk(items, 5);
    
    int results[5];     // Could also be any iterator
    size_t count = q.try_dequeue_bulk(results, 5);
    for (size_t i = 0; i != count; ++i) {
        assert(results[i] == items[i]);
    }

#### Preallocation (correctly using `try_enqueue`)

`try_enqueue`, unlike just plain `enqueue`, will never allocate memory. If there's not enough room in the
queue, it simply returns false. The key to using this method properly, then, is to ensure enough space is
pre-allocated for your desired maximum element count.

The constructor accepts a count of the number of elements that it should reserve space for. Because the
queue works with blocks of elements, however, and not individual elements themselves, the value to pass
in order to obtain an effective number of pre-allocated element slots is non-obvious.

First, be aware that the count passed is rounded up to the next multiple of the block size. Note that the
default block size is 32 (this can be changed via the traits). Second, once a slot in a block has been
enqueued to, that slot cannot be re-used until the rest of the block has completely been completely filled
up and then completely emptied. This affects the number of blocks you need in order to account for the
overhead of partially-filled blocks. Third, each producer (whether implicit or explicit) claims and recycles
blocks in a different manner, which again affects the number of blocks you need to account for a desired number of
usable slots.

Suppose you want the queue to be able to hold at least `N` elements at any given time. Without delving too
deep into the rather arcane implementation details, here are some simple formulas for the number of elements
to request for pre-allocation in such a case. Note the division is intended to be arithmetic division and not
integer division (in order for `ceil()` to work).

For explicit producers (using tokens to enqueue):

    (ceil(N / BLOCK_SIZE) + 1) * MAX_NUM_PRODUCERS * BLOCK_SIZE

For implicit producers (no tokens):

    (ceil(N / BLOCK_SIZE) - 1 + 2 * MAX_NUM_PRODUCERS) * BLOCK_SIZE

When using mixed producer types:

    ((ceil(N / BLOCK_SIZE) - 1) * (MAX_EXPLICIT_PRODUCERS + 1) + 2 * (MAX_IMPLICIT_PRODUCERS + MAX_EXPLICIT_PRODUCERS)) * BLOCK_SIZE

If these formulas seem rather inconvenient, you can use the constructor overload that accepts the minimum
number of elements (`N`) and the maximum number of explicit and implicit producers directly, and let it do the
computation for you.

Finally, it's important to note that because the queue is only eventually consistent and takes advantage of
weak memory ordering for speed, there's always a possibility that under contention `try_enqueue` will fail
even if the queue is correctly pre-sized for the desired number of elements. (e.g. A given thread may think that
the queue's full even when that's no longer the case.) So no matter what, you still need to handle the failure
case (perhaps looping until it succeeds), unless you don't mind dropping elements.

#### Exception safety

The queue is exception safe, and will never become corrupted if used with a type that may throw exceptions.
The queue itself never throws any exceptions (operations fail gracefully (return false) if memory allocation
fails instead of throwing `std::bad_alloc`).

It is important to note that the guarantees of exception safety only hold if the element type never throws
from its destructor, and that any iterators passed into the queue (for bulk operations) never throw either.
Note that in particular this means `std::back_inserter` iterators must be used with care, since the vector
being inserted into may need to allocate and throw a `std::bad_alloc` exception from inside the iterator;
so be sure to reserve enough capacity in the target container first if you do this.

The guarantees are presently as follows:
- Enqueue operations are rolled back completely if an exception is thrown from an element's constructor.
  For bulk enqueue operations, this means that elements are copied instead of moved (in order to avoid
  having only some of the objects be moved in the event of an exception). Non-bulk enqueues always use
  the move constructor if one is available.
- If the assignment operator throws during a dequeue operation (both single and bulk), the element(s) are
  considered dequeued regardless. In such a case, the dequeued elements are all properly destructed before
  the exception is propagated, but there's no way to get the elements themselves back.
- Any exception that is thrown is propagated up the call stack, at which point the queue is in a consistent
  state.

Note: If any of your type's copy constructors/move constructors/assignment operators don't throw, be sure
to annotate them with `noexcept`; this will avoid the exception-checking overhead in the queue where possible
(even with zero-cost exceptions, there's still a code size impact that has to be taken into account).

#### Traits

The queue also supports a traits template argument which defines various types, constants,
and the memory allocation and deallocation functions that are to be used by the queue. The typical pattern
to providing your own traits is to create a class that inherits from the default traits
and override only the values you wish to change. Example:

    struct MyTraits : public moodycamel::ConcurrentQueueDefaultTraits
    {
    	static const size_t BLOCK_SIZE = 256;		// Use bigger blocks
    };
    
    moodycamel::ConcurrentQueue<int, MyTraits> q;

#### How to dequeue types without calling the constructor

The normal way to dequeue an item is to pass in an existing object by reference, which
is then assigned to internally by the queue (using the move-assignment operator if possible).
This can pose a problem for types that are
expensive to construct or don't have a default constructor; fortunately, there is a simple
workaround: Create a wrapper class that copies the memory contents of the object when it
is assigned by the queue (a poor man's move, essentially). Note that this only works if
the object contains no internal pointers. Example:

    struct MyObjectMover {
        inline void operator=(MyObject&& obj) {
            std::memcpy(data, &obj, sizeof(MyObject));
            
            // TODO: Cleanup obj so that when it's destructed by the queue
            // it doesn't corrupt the data of the object we just moved it into
        }

        inline MyObject& obj() { return *reinterpret_cast<MyObject*>(data); }

    private:
        align(alignof(MyObject)) char data[sizeof(MyObject)];
    };

A less dodgy alternative, if moves are cheap but default construction is not, is to use a
wrapper that defers construction until the object is assigned, enabling use of the move
constructor:

    struct MyObjectMover {
        inline void operator=(MyObject&& x) {
            new (data) MyObject(std::move(x));
            created = true;
        }

        inline MyObject& obj() {
            assert(created);
            return *reinterpret_cast<MyObject*>(data);
        }

        ~MyObjectMover() {
            if (created)
                obj().~MyObject();
        }

    private:
        align(alignof(MyObject)) char data[sizeof(MyObject)];
        bool created = false;
    };

## Samples

There are some more detailed samples [here][samples.md]. The source of
the [unit tests][unittest-src] and [benchmarks][benchmark-src] are available for reference as well.

## Benchmarks

See my blog post for some [benchmark results][benchmarks] (including versus `boost::lockfree::queue` and `tbb::concurrent_queue`),
or run the benchmarks yourself (requires MinGW and certain GnuWin32 utilities to build on Windows, or a recent
g++ on Linux):

    cd build
    make benchmarks
    bin/benchmarks

The short version of the benchmarks is that it's so fast (especially the bulk methods), that if you're actually
using the queue to *do* anything, the queue won't be your bottleneck.

## Tests (and bugs)

I've written quite a few unit tests as well as a randomized long-running fuzz tester. I also ran the
core queue algorithm through the [CDSChecker][cdschecker] C++11 memory model model checker. Some of the
inner algorithms were tested separately using the [Relacy][relacy] model checker, and full integration
tests were also performed with Relacy.
I've tested
on Linux (Fedora 19) and Windows (7), but only on x86 processors so far (Intel and AMD). The code was
written to be platform-independent, however, and should work across all processors and OSes.

Due to the complexity of the implementation and the difficult-to-test nature of lock-free code in general,
there may still be bugs. If anyone is seeing buggy behaviour, I'd like to hear about it! (Especially if
a unit test for it can be cooked up.) Just open an issue on GitHub.

## License

I'm releasing the source of this repository (with the exception of third-party code, i.e. the Boost queue
(used in the benchmarks for comparison), Intel's TBB library (ditto), CDSChecker, Relacy, and Jeff Preshing's
cross-platform semaphore, which all have their own licenses)
under a simplified BSD license. I'm also dual-licensing under the Boost Software License.
See the [LICENSE.md][license] file for more details.

Note that lock-free programming is a patent minefield, and this code may very
well violate a pending patent (I haven't looked), though it does not to my present knowledge.
I did design and implement this queue from scratch.

## Diving into the code

If you're interested in the source code itself, it helps to have a rough idea of how it's laid out. This
section attempts to describe that.

The queue is formed of several basic parts (listed here in roughly the order they appear in the source). There's the
helper functions (e.g. for rounding to a power of 2). There's the default traits of the queue, which contain the
constants and malloc/free functions used by the queue. There's the producer and consumer tokens. Then there's the queue's
public API itself, starting with the constructor, destructor, and swap/assignment methods. There's the public enqueue methods,
which are all wrappers around a small set of private enqueue methods found later on. There's the dequeue methods, which are
defined inline and are relatively straightforward.

Then there's all the main internal data structures. First, there's a lock-free free list, used for recycling spent blocks (elements
are enqueued to blocks internally). Then there's the block structure itself, which has two different ways of tracking whether
it's fully emptied or not (remember, given two parallel consumers, there's no way to know which one will finish first) depending on where it's used.
Then there's a small base class for the two types of internal SPMC producer queues (one for explicit producers that holds onto memory
but attempts to be faster, and one for implicit ones which attempt to recycle more memory back into the parent but is a little slower).
The explicit producer is defined first, then the implicit one. They both contain the same general four methods: One to enqueue, one to
dequeue, one to enqueue in bulk, and one to dequeue in bulk. (Obviously they have constructors and destructors too, and helper methods.)
The main difference between them is how the block handling is done (they both use the same blocks, but in different ways, and map indices
to them in different ways).

Finally, there's the miscellaneous internal methods: There's the ones that handle the initial block pool (populated when the queue is constructed),
and an abstract block pool that comprises the initial pool and any blocks on the free list. There's ones that handle the producer list
(a lock-free add-only linked list of all the producers in the system). There's ones that handle the implicit producer lookup table (which
is really a sort of specialized TLS lookup). And then there's some helper methods for allocating and freeing objects, and the data members
of the queue itself, followed lastly by the free-standing swap functions.


[blog]: http://moodycamel.com/blog/2014/a-fast-general-purpose-lock-free-queue-for-c++
[design]: http://moodycamel.com/blog/2014/detailed-design-of-a-lock-free-queue
[samples.md]: https://github.com/cameron314/concurrentqueue/blob/master/samples.md
[source]: https://github.com/cameron314/concurrentqueue
[concurrentqueue.h]: https://github.com/cameron314/concurrentqueue/blob/master/concurrentqueue.h
[blockingconcurrentqueue.h]: https://github.com/cameron314/concurrentqueue/blob/master/blockingconcurrentqueue.h
[unittest-src]: https://github.com/cameron314/concurrentqueue/tree/master/tests/unittests
[benchmarks]: http://moodycamel.com/blog/2014/a-fast-general-purpose-lock-free-queue-for-c++#benchmarks
[benchmark-src]: https://github.com/cameron314/concurrentqueue/tree/master/benchmarks
[license]: https://github.com/cameron314/concurrentqueue/blob/master/LICENSE.md
[cdschecker]: http://demsky.eecs.uci.edu/c11modelchecker.html
[relacy]: http://www.1024cores.net/home/relacy-race-detector
[spsc]: https://github.com/cameron314/readerwriterqueue
[salsa]: http://webee.technion.ac.il/~idish/ftp/spaa049-gidron.pdf
cmake_minimum_required(VERSION 3.9)
project(concurrentqueue VERSION 1.0.0)

include(GNUInstallDirs)

add_library(${PROJECT_NAME} INTERFACE)

target_include_directories(concurrentqueue INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})

install(FILES blockingconcurrentqueue.h concurrentqueue.h lightweightsemaphore.h LICENSE.md
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME})

This license file applies to everything in this repository except that which
is explicitly annotated as being written by other authors, i.e. the Boost
queue (included in the benchmarks for comparison), Intel's TBB library (ditto),
dlib::pipe (ditto),
the CDSChecker tool (used for verification), the Relacy model checker (ditto),
and Jeff Preshing's semaphore implementation (used in the blocking queue) which
has a zlib license (embedded in lightweightsempahore.h).

---

Simplified BSD License:

Copyright (c) 2013-2016, Cameron Desrochers.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this list of
conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice, this list of
conditions and the following disclaimer in the documentation and/or other materials
provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

---

I have also chosen to dual-license under the Boost Software License as an alternative to
the Simplified BSD license above:

Boost Software License - Version 1.0 - August 17th, 2003

Permission is hereby granted, free of charge, to any person or organization
obtaining a copy of the software and accompanying documentation covered by
this license (the "Software") to use, reproduce, display, distribute,
execute, and transmit the Software, and to prepare derivative works of the
Software, and to permit third-parties to whom the Software is furnished to
do so, all subject to the following:

The copyright notices in the Software and this entire statement, including
the above license grant, this restriction and the following disclaimer,
must be included in all copies of the Software, in whole or in part, and
all derivative works of the Software, unless such copies or derivative
works are solely in the form of machine-executable object code generated by
a source language processor.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
This is a partial copy of the Intel TBB open source version.
The version taken is 4.3, obtained from https://www.threadingbuildingblocks.org/download
The files in this directory consist of the files taken from src/tbb and include/tbbThis is a partial copy of Boost 1.60, specifically only the parts that
boost/lockfree/queue.hpp depends on (extracted using bcp).Boost Software License - Version 1.0 - August 17th, 2003

Permission is hereby granted, free of charge, to any person or organization
obtaining a copy of the software and accompanying documentation covered by
this license (the "Software") to use, reproduce, display, distribute,
execute, and transmit the Software, and to prepare derivative works of the
Software, and to permit third-parties to whom the Software is furnished to
do so, all subject to the following:

The copyright notices in the Software and this entire statement, including
the above license grant, this restriction and the following disclaimer,
must be included in all copies of the Software, in whole or in part, and
all derivative works of the Software, unless such copies or derivative
works are solely in the form of machine-executable object code generated by
a source language processor.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
#error "Don't put the dlib folder in your include path"
/*
  You are getting this error because you have added the dlib folder to your
  compiler's include search path.  

  You should *NOT* add the dlib folder itself to your compiler's include path. 
  Doing so will cause the build to fail because of name collisions (such as 
  dlib/string.h and string.h from the standard library). Instead you should 
  add the folder that contains the dlib folder to your include search path 
  and then use include statements of the form #include <dlib/queue.h> or
  #include "dlib/queue.h".  This will ensure that everything builds correctly.

  XCode:
  	The XCode IDE often puts all folders that it knows about into 
	the compiler search path.  So if you are using XCode then either 
	don't drag the whole dlib folder into the project or alternatively 
	modify your XCode project settings to not auto-add all folders to 
	the include path.  Instead just make sure that the dlib folder is 
	itself inside a folder in your include path.  
*/
#error "Don't write #include <dlib/all/source.cpp> in your code."
/*
  In C++, it is generally an error to #include .cpp files.  This is because it
  can lead to what are called multiply defined symbol errors.  Therefore, you
  should compile dlib/all/source.cpp into your application just like you would
  compile any other .cpp file.  
  
  If you are using Visual Studio you add .cpp files to your application using
  the solution explorer window.  Specifically, right click on Source Files,
  then select Add -> Existing Item and select the .cpp files you want to add.

  For general information on compiling dlib see http://dlib.net/compile.html
*/
These tests require CDSChecker to be checked out into a subdirectory
named 'model-checker'.

CDSChecker can be obtained from: git://demsky.eecs.uci.edu/model-checker.git
The version last used for testing was: da671f78d0aa057272bb82f580b36a188b6331bd
Relacy Race Detector
Copyright (c) 2008-2013, Dmitry S. Vyukov
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
  - Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions
    and the following disclaimer in the documentation and/or other materials provided with the distribution.
  - The name of the owner may not be used to endorse or promote products derived from this software
    without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE OWNER "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE OWNER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
Test parameters. You can specify various parameters for test.
rl::test_params p;
p.search_type = rl::fair_context_bound_scheduler_type;
p.context_bound = 1;
p.execution_depth_limit = 1000;
rl::simulate<test_t>(p);

The main parameter is scheduler type used for simulation. There is 3 types of scheduler:
random_scheduler_type - random exploration of state space
fair_full_search_scheduler_type - exhaustive systematic exploration of state space
fair_context_bound_scheduler_type - systematic exploration of state space with limit on context switches.

For random_scheduler_type you can specify 'iteration_count' parameter - number of explored executions.
For fair_context_bound_scheduler_type you can specify 'context_bound' parameter - limit on context switches.

Also you can specify 'execution_depth_limit' parameter - used for livelock detection. All executions with trace longer than execution_depth_limit will be treated as livelocked (or non-terminating).

Also from test_params structure you can receive output parameters from simulation. Main output parameter is 'test_result' which describes cause of test failure.

If you use fair_full_search_scheduler_type or fair_context_bound_scheduler_type, in order to ensure fairness of scheduler, you must use 'yield' calls in all 'spin-loops', otherwise simulation will report non-terminating execution. Example:

struct race_seq_ld_ld_test : rl::test_suite<race_seq_ld_ld_test, 2>
{
    std::atomic<int> a;
    rl::var<int> x;

    void before()
    {
        a($) = 0;
        x($) = 0;
    }

    void thread(unsigned index)
    {
        if (index)
        {
            x($).load();
            a($).store(1, std::memory_order_relaxed);
        }
        else
        {
            rl::backoff b;
            while (0 == a($).load(rl::memory_order_relaxed))
                  b.yield($);
            x($).load();
        }
    }
};



 - Relaxed ISO C++0x Memory Model. Relaxed/acquire/release/acq_rel/seq_cst memory operations. The only non-supported feature is memory_order_consume, it's simulated with memory_order_acquire.
 - Exhaustive automatic error checking (including ABA detection).
 - Full-fledged atomics library (with spurious failures in compare_exchange()).
 - Memory fences.
 - Arbitrary number of threads.
 - Detailed execution history for failed tests.
 - No false positives.
 - Before/after/invariant functions for test suites.

1. Add
#include <relacy/relacy_std.hpp>

2. For atomic variables use type std::atomic<T>:
std::atomic<void*> head;

3. For usual non-atomic variables use type rl::var<T>:
rl::var<int> data;
Such vars will be checked for races and included into trace.

4. All accesses to std::atomic<T> and rl::var<T> variables postfix with '($)':
std::atomic<void*> head;
rl::var<int> data;
head($).store(0);
data($) = head($).load();

5. Strictly thread-private variables use can leave as-is:
for (int i = 0; i != 10; ++i)
Such vars will be NOT checked for races NOR included into trace. But they will accelerate verification.

6. Describe test-suite: number of threads, thread function, before/after/invariant functions. See example below.

7. Place asserts:
int x = g($).load();
RL_ASSERT(x > 0);

8. Start verification:
rl::simulate<test_suite_t>();

Here is complete example:

#include <relacy/relacy_std.hpp>

// template parameter '2' is number of threads
struct race_test : rl::test_suite<race_test, 2>
{
    std::atomic<int> a;
    rl::var<int> x;

    // executed in single thread before main thread function
    void before()
    {
        a($) = 0;
        x($) = 0;
    }

    // main thread function
    void thread(unsigned thread_index)
    {
        if (0 == thread_index)
        {
            x($) = 1;
            a($).store(1, rl::memory_order_relaxed);
        }
        else
        {
            if (1 == a($).load(rl::memory_order_relaxed))
                x($) = 2;
        }
    }

    // executed in single thread after main thread function
    void after()
    {
    }

    // executed in single thread after every 'visible' action in main threads
    // disallowed to modify any state
    void invariant()
    {
    }
};

int main()
{
    rl::simulate<race_test>();
}



Relacy Race Detector Todo List:

- use indirection and indices for TLS, because on Windows TLS index is DWORD (not DWORD_PTR) (eliminate pointers?)
+ provide rl::hash_ptr()
- support for fair timed waits
+ remove iteration count estimation from full sched -> causes division by 0
- history: memory allocation before object ctor (new T (...))
+ code in test::after() affects iteration count with full scheduler -> final and estimated iteration counts are the same

- non-deterministic sub-expression calculation:
foo(bar.load(std::memory_order_acquire), baz.load(std::memory_order_acquire));

- post issue:
can't simulate some modification orders in presence of data-races-type-2 for atomic vars:
//thread 1
x.store(1, std::memory_order_relaxed);
y.store(1, std::memory_order_relaxed);
//thread 2
while (y.load(std::memory_order_relaxed) == 0
{}
x.store(2, std::memory_order_relaxed);
-> modification order of 'x' will never be "2, 1"


 [CORE]
- initially run threads one by one
- initially run some iterations twice, in order to check that unit-test is deterministic
? add unique identifiers to atomics, vars, mutexes etc (address can be useful too)
- example catalog (description, used techniques, what error is found)
- do I need sched() before atomic loads?
- do I need sched() before mutex unlock?
- for loads output in history value of which store is loaded
- detect dead-code
- output which operations cause data race
? output happens-before matrix, synchronizes-with matrix etc
- SEH handler to catch paging faults
- sched before malloc/free to allow more ABA

 [PERF]
- implement performance simulation
 - cacheline transfers
 - atomic rmw operations
 - fences

[OTHER]
- parallelize the run-time for random scheduler
- parallelize the run-time for tree search scheduler
- manual control over scheduler
- persistent checkpointing of scheduler state (to allow "continue")
- atomic blocks (pdr implementation -> pdr component)
? state space reductions (sleep sets, dynamic persistent sets)
? what can I do with serialization points -> user specifies "visible" results
    system checks for linearizablity -> "visible" results equal to some sequential execution
? save program state inside iteration (save point), continue other iterations from this save point 
? partial order reductions by memorizing happens-before graphs, not program state
? estimate progress by seeing how many iterations it gets to move 0->1 on some stree level
? lower bound, upper bound, mean of progress

O(X) = (P^(C + 3)) * (N^(P + C + 1)) * (P + C)!

 - Race condition (accoring to ISO C++0x)
 - Access to uninitialized variable
 - Access to freed memory
 - Double free
 - Memory leak
 - Deadlock
 - Livelock
 - User assert failed
 - User invariant failed

