import heapq
# input = open("input.txt").readline
q = int(input())

scoring_machines = []
heap_queue = []
queue = []
domains = []
start_history = {}
end_history = {}

def prepare(info):
    global scoring_machines
    n, u0 = info

    scoring_machines = [None] * int(n)

    heapq.heappush(heap_queue, [1, 0, u0])
    queue.append(u0)


def request(info):
    # t초에 채점 우선순위가 p이면서 url이 u인 문제에 대한 채점 요청이 들어오게 됩니다. 
    t, p, u = info

    # 채점 task는 채점 대기 큐에 들어가게 됩니다. 채점 대기 큐에 이미 u가 있으면 큐에 추가하지 않고 넘어감
    if u not in queue:
        heapq.heappush(heap_queue, [int(p), int(t), u])
        queue.append(u)


def try_scoring(info):
    if None not in scoring_machines:
        return

    t = info[0]
    temp = []
    started = False
    # for i in range(len(heap_queue)):
    #     p_heap, t_heap, u_heap = heapq.heappop(heap_queue)

    #     domain = u_heap.split("/")[0]

    #     # 도메인이 채점중이면 못들어감
    #     if domain in domains:
    #         temp.append([p_heap, t_heap, u_heap])
    #         heapq.heapify(heap_queue)
    #         continue

    #     # 채점중은 아닌데 최근에 채점했으면 못들어감
    #     elif domain in start_history and domain in end_history:
    #         gap = end_history[domain] - start_history[domain]

    #         if int(t) < (start_history[domain] + 3 * gap):
    #             temp.append([p_heap, t_heap, u_heap])
    #             continue
        
    #     # 채점 시작
    #     for j, s in enumerate(scoring_machines):
    #         if s == None:
    #             scoring_machines[j] = u_heap
    #             queue.remove(u_heap)
    #             domains.append(domain)
    #             start_history[domain] = int(t)
    #             if domain in end_history:
    #                 del(end_history[domain])
    #             started = True
    #             break
                
    #     if started:
    #         break

    # for t in temp:
    #     heapq.heappush(heap_queue, t)

    for i in range(len(heap_queue)):
        p_heap, t_heap, u_heap = heap_queue[i]

        domain = u_heap.split("/")[0]

        # 도메인이 채점중이면 못들어감
        if domain in domains:
            continue

        # 채점중은 아닌데 최근에 채점했으면 못들어감
        elif domain in start_history and domain in end_history:
            gap = end_history[domain] - start_history[domain]
            if int(t) < (start_history[domain] + 3 * gap):
                continue
        
        # 채점 시작
        for j, s in enumerate(scoring_machines):
            if s == None:
                # print(heap_queue)
                # print(queue, u_heap)
                del heap_queue[i]
                queue.remove(u_heap)
                scoring_machines[j] = u_heap
                domains.append(domain)
                start_history[domain] = int(t)
                if domain in end_history:
                    del(end_history[domain])
                started = True
                break
                
        if started:
            break


def terminate(info):
    t, j_id = info
    jid = int(j_id)
    # print("machine", scoring_machines[j_id-1])

    if scoring_machines[jid-1] != None:
        url = scoring_machines[jid-1]
        domain = url.split("/")[0]
        domains.remove(domain)
        end_history[domain] = int(t)
        scoring_machines[jid-1] = None


for i in range(q):
    ins, *info = input().split()
    # print(i)
    if ins == '100':
        # print(ins, info)
        prepare(info)
        # print("heap_queue", heap_queue)
        # print("queue", queue)
        # print("machine", scoring_machines)
    elif ins == '200':  # 요청
        # print(ins, info)
        request(info)
        # print("heap_queue", heap_queue)
        # print("queue", queue)
        # print("machine", scoring_machines)
    elif ins == '300':  # 채점시도
        # print(ins, info)
        try_scoring(info)
        # print("heap_queue", heap_queue)
        # print("queue", queue)
        # print("machine", scoring_machines)
    elif ins == '400':  # 채점종료
        # print(ins, info)
        terminate(info)
        # print("heap_queue", heap_queue)
        # print("queue", queue)
        # print("machine", scoring_machines)
    else:               # 프린트
        # print(ins)
        print(len(heap_queue))
        # 시간 t에 채점 대기 큐에 있는 채점 태스크의 수 출력
    # print()