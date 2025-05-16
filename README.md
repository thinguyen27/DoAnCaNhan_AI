# 8-Puzzle Solver
#Họ và tên: Nguyễn Trần Quốc Thi
#MSSV: 23110331
## Giới thiệu trò chơi 8-Puzzle

8-Puzzle là trò chơi giải đố trên bảng 3x3 gồm 8 ô số và 1 ô trống, nhiệm vụ là di chuyển các ô để đạt được trạng thái đích đã định (thường là sắp xếp theo thứ tự từ 1 đến 8, ô trống ở cuối). Bài toán này là ví dụ điển hình của bài toán tìm kiếm trạng thái trong Trí tuệ nhân tạo (AI).

---

## Các nhóm thuật toán giải 8-Puzzle

### 1. Nhóm thuật toán Uninformed Search (Tìm kiếm không thông tin)
Uninformed Search (tìm kiếm không thông tin) là nhóm các thuật toán tìm kiếm trạng thái mà không sử dụng thêm bất kỳ thông tin bổ sung nào về khoảng cách hoặc chi phí đến trạng thái mục tiêu. Nói cách khác, thuật toán chỉ biết cấu trúc trạng thái và các phép toán chuyển trạng thái mà không có “gợi ý” hay ước lượng nào giúp định hướng tìm kiếm.
#### BFS (Breadth-First Search)
![BFS gif](https://github.com/user-attachments/assets/17003069-c69d-4aa9-8569-400f867e79b8)

- **Cách chạy:**  
  Mở rộng các nút theo từng mức độ (độ sâu) từ trạng thái ban đầu. Tất cả trạng thái ở mức độ hiện tại được khám phá trước khi chuyển sang mức độ sâu hơn. Dùng hàng đợi FIFO để lưu các trạng thái chờ khám phá.  
- **Ưu điểm:**  
  - Đảm bảo tìm lời giải ngắn nhất (số bước di chuyển ít nhất).  
  - Thuật toán đơn giản, dễ triển khai.  
- **Nhược điểm:**  
  - Tốn bộ nhớ lớn vì phải lưu toàn bộ các trạng thái ở mức độ hiện tại.  
  - Có thể rất chậm với không gian trạng thái lớn.

#### DFS (Depth-First Search)
![DFS](https://github.com/user-attachments/assets/955563b5-4909-48c8-acd4-2164fd0b7c91)

- **Cách chạy:**  
  Khám phá sâu một nhánh cho đến khi không còn trạng thái mới hoặc đến độ sâu giới hạn, sau đó quay lui (backtrack) để khám phá nhánh khác. Dùng ngăn xếp (stack) để lưu trạng thái.  
- **Ưu điểm:**  
  - Tốn ít bộ nhớ hơn BFS (chỉ cần lưu đường đi hiện tại).  
  - Thường nhanh trong không gian tìm kiếm sâu.  
- **Nhược điểm:**  
  - Không đảm bảo tìm lời giải ngắn nhất.  
  - Có thể rơi vào vòng lặp vô tận nếu không giới hạn độ sâu.

#### IDS (Iterative Deepening Search)
![IDS](https://github.com/user-attachments/assets/2ec411bc-a0ab-4f0e-a339-f8b307fc4c35)

- **Cách chạy:**  
  Thực hiện DFS với độ sâu giới hạn tăng dần từ 0 lên, mỗi lần chạy DFS từ đầu đến giới hạn độ sâu mới, đến khi tìm được lời giải.  
- **Ưu điểm:**  
  - Kết hợp ưu điểm của BFS (tìm lời giải ngắn nhất) và DFS (tốn ít bộ nhớ).  
  - Tốn bộ nhớ thấp hơn BFS nhiều.  
- **Nhược điểm:**  
  - Phải lặp lại nhiều lần DFS gây tốn thời gian.

#### UCS (Uniform Cost Search)
![UCS](https://github.com/user-attachments/assets/5d7ce85b-a23a-4f22-949e-39a6d3ef5c8c)

- **Cách chạy:**  
  Mở rộng nút có chi phí đường đi thấp nhất hiện có (tính tổng chi phí từ gốc đến nút hiện tại). Sử dụng hàng đợi ưu tiên (priority queue) dựa trên chi phí.  
- **Ưu điểm:**  
  - Đảm bảo tìm lời giải tối ưu về chi phí (nếu chi phí di chuyển khác nhau).  
- **Nhược điểm:**  
  - Tốn bộ nhớ và thời gian lớn nếu chi phí nhiều khác biệt.

---

### 2. Nhóm thuật toán Informed Search (Tìm kiếm có thông tin)
Informed Search (tìm kiếm có thông tin) là nhóm các thuật toán tìm kiếm sử dụng thông tin bổ sung (thường là heuristic — ước lượng chi phí hoặc khoảng cách từ trạng thái hiện tại đến mục tiêu) để định hướng quá trình tìm kiếm, giúp thuật toán tìm lời giải nhanh hơn và hiệu quả hơn so với các thuật toán uninformed search.
#### Greedy Search
![Greedy](https://github.com/user-attachments/assets/7e50d71b-b9b3-4507-a277-42a7365af29c)

- **Cách chạy:**  
  Tại mỗi bước chọn trạng thái con có giá trị heuristic (ước lượng khoảng cách đến đích) nhỏ nhất, không xét chi phí đường đi đã đi.  
- **Ưu điểm:**  
  - Thường nhanh và đơn giản.  
- **Nhược điểm:**  
  - Không đảm bảo tìm lời giải tối ưu hay thậm chí lời giải.  
  - Dễ rơi vào bẫy heuristic sai lệch.

#### A*
![A](https://github.com/user-attachments/assets/55cc8a14-6db4-445e-8b3d-5d4f9ee0bec2)

- **Cách chạy:**  
  Mở rộng trạng thái có tổng chi phí ước lượng \( f(n) = g(n) + h(n) \), trong đó:  
  - \(g(n)\) là chi phí thực tế từ trạng thái gốc đến trạng thái hiện tại \(n\).  
  - \(h(n)\) là heuristic ước lượng chi phí còn lại đến đích.  
  Sử dụng hàng đợi ưu tiên theo giá trị \(f(n)\).  
- **Ưu điểm:**  
  - Đảm bảo tìm lời giải tối ưu nếu heuristic hợp lệ (không đánh giá vượt).  
  - Tìm kiếm hiệu quả hơn uninformed search.  
- **Nhược điểm:**  
  - Tốn bộ nhớ lớn, có thể chậm với trạng thái lớn.

#### IDA* (Iterative Deepening A*)
![IDAstar](https://github.com/user-attachments/assets/809d75eb-90e8-47f5-9b14-80e7b8e43216)

- **Cách chạy:**  
  Kết hợp iterative deepening với A*, giới hạn ngưỡng \(f\) tăng dần qua các lần lặp để giảm bộ nhớ.  
- **Ưu điểm:**  
  - Giảm bộ nhớ so với A*.  
  - Vẫn đảm bảo tối ưu nếu heuristic hợp lệ.  
- **Nhược điểm:**  
  - Có thể chậm do lặp lại nhiều lần.

---

### 3. Nhóm thuật toán Local Search (Tìm kiếm cục bộ)
Local Search (tìm kiếm cục bộ) là nhóm thuật toán tìm kiếm không duyệt toàn bộ không gian trạng thái mà tập trung cải thiện dần trạng thái hiện tại bằng cách di chuyển sang các trạng thái láng giềng gần đó.
#### Simple Hill Climbing

- **Cách chạy:**  
  Từ trạng thái hiện tại, chọn ngẫu nhiên một trạng thái láng giềng có giá trị heuristic tốt hơn và di chuyển tới đó, lặp lại cho đến khi không còn trạng thái láng giềng tốt hơn.  
- **Ưu điểm:**  
  - Đơn giản, nhanh.  
- **Nhược điểm:**  
  - Dễ bị kẹt ở cực trị địa phương.  
  - Không đảm bảo tìm lời giải tối ưu.

#### Steepest Ascent Hill Climbing

- **Cách chạy:**  
  Tại mỗi bước, xem xét tất cả trạng thái láng giềng và chọn trạng thái tốt nhất (giá trị heuristic thấp nhất) để di chuyển.  
- **Ưu điểm:**  
  - Luôn chọn bước cải thiện nhất.  
- **Nhược điểm:**  
  - Vẫn có thể bị kẹt cực trị địa phương.

#### Stochastic Hill Climbing

- **Cách chạy:**  
  Từ các trạng thái láng giềng tốt hơn hiện tại, chọn ngẫu nhiên một trạng thái để di chuyển.  
- **Ưu điểm:**  
  - Giảm khả năng kẹt cực trị địa phương hơn simple và steepest.  
- **Nhược điểm:**  
  - Kết quả không ổn định, phụ thuộc may rủi.

#### Beam Search
![Beam](https://github.com/user-attachments/assets/f4a8f4e0-a3ac-4bc6-8cec-cad5b74504d0)

- **Cách chạy:**  
  Duy trì một tập (beam) gồm các trạng thái tốt nhất (theo heuristic) mỗi bước, mở rộng tất cả trạng thái này để tìm trạng thái con, chọn lại top trạng thái tốt nhất cho bước kế tiếp.  
- **Ưu điểm:**  
  - Giảm bộ nhớ so với BFS.  
  - Điều chỉnh linh hoạt beam width để cân bằng giữa độ chính xác và tài nguyên.  
- **Nhược điểm:**  
  - Có thể bỏ lỡ lời giải nếu beam width quá nhỏ.

#### Simulated Annealing

- **Cách chạy:**  
  Từ trạng thái hiện tại, chọn ngẫu nhiên một trạng thái láng giềng; nếu tốt hơn thì di chuyển, nếu kém hơn thì chấp nhận với xác suất giảm dần theo "nhiệt độ" (temperature) giảm dần theo thời gian, giúp thoát khỏi cực trị địa phương.  
- **Ưu điểm:**  
  - Có khả năng tìm lời giải toàn cục cao hơn hill climbing.  
- **Nhược điểm:**  
  - Cần tinh chỉnh các tham số (nhiệt độ, tỷ lệ giảm nhiệt).  
  - Chậm hơn so với các thuật toán đơn giản.

#### Genetic Algorithm (GA)

- **Cách chạy:**  
  Tạo quần thể các lời giải (cá thể), đánh giá fitness, lai ghép (crossover) và đột biến (mutation) qua nhiều thế hệ để tiến tới lời giải tốt hơn.  
- **Ưu điểm:**  
  - Thích hợp với không gian trạng thái lớn, phức tạp.  
  - Đa dạng lời giải, giảm khả năng rơi vào cực trị địa phương.  
- **Nhược điểm:**  
  - Cần thiết lập nhiều tham số (kích thước quần thể, tỉ lệ đột biến, số thế hệ).  
  - Không đảm bảo tìm lời giải tối ưu.

---

### 4. Nhóm thuật toán cho môi trường phức tạp (Complex Environment)
Nhóm thuật toán cho môi trường phức tạp (Complex Environment) là các thuật toán được thiết kế để giải quyết bài toán tìm kiếm trong những môi trường mà trạng thái không chỉ đơn giản mà còn có thể bị bất định, không chắc chắn, hoặc có nhiều khả năng kết hợp phức tạp.
#### Belief State Search

- **Cách chạy:**  
  Tìm kiếm trên không gian các trạng thái tin tưởng (belief states) biểu diễn tập hợp các trạng thái có thể xảy ra khi thông tin không chắc chắn hoặc quan sát bị hạn chế. Thuật toán mở rộng các trạng thái theo độ tin cậy và khả năng đạt mục tiêu.  
- **Ưu điểm:**  
  - Xử lý được bài toán có thông tin không đầy đủ, môi trường không chắc chắn.  
- **Nhược điểm:**  
  - Không gian trạng thái lớn, phức tạp.  
  - Thuật toán nặng về tính toán và bộ nhớ.

#### AND-OR Search

- **Cách chạy:**  
  Mở rộng cây tìm kiếm bao gồm nút AND (yêu cầu tất cả các con đều thỏa) và nút OR (chỉ cần một con thỏa), phù hợp với bài toán có nhiều khả năng hoặc kết quả phụ thuộc đa dạng.  
- **Ưu điểm:**  
  - Thích hợp cho bài toán có cấu trúc phức tạp, nhiều tình huống lựa chọn kết hợp.  
- **Nhược điểm:**  
  - Thuật toán phức tạp, đòi hỏi tài nguyên lớn.

---

### 5. Nhóm thuật toán CSP (Constraint Satisfaction Problems)
Nhóm thuật toán CSP (Constraint Satisfaction Problems) là tập các thuật toán được thiết kế để giải các bài toán thỏa mãn ràng buộc, trong đó cần tìm cách gán giá trị cho một tập biến sao cho tất cả các ràng buộc giữa các biến được thỏa mãn.
#### Backtracking

- **Cách chạy:**  
  Gán lần lượt giá trị cho từng biến, nếu vi phạm ràng buộc thì quay lui (backtrack) thử giá trị khác. Tiếp tục cho đến khi gán đủ biến hoặc không còn giá trị khả thi.  
- **Ưu điểm:**  
  - Đơn giản, đảm bảo tìm lời giải nếu tồn tại.  
- **Nhược điểm:**  
  - Có thể rất chậm và tốn nhiều thời gian khi không gian tìm kiếm lớn.

#### Backtracking with Forward Checking

- **Cách chạy:**  
  Mở rộng Backtracking bằng cách, sau khi gán biến, kiểm tra sớm tính nhất quán của các biến chưa gán (loại bỏ các giá trị vi phạm khỏi miền giá trị) để tránh đi vào nhánh vô vọng.  
- **Ưu điểm:**  
  - Giảm đáng kể số lần quay lui.  
  - Tăng hiệu quả tìm kiếm.  
- **Nhược điểm:**  
  - Phức tạp hơn trong triển khai.  
  - Vẫn có thể tốn thời gian nếu bài toán lớn.

---

## Cách sử dụng chương trình

- Chọn thuật toán muốn chạy trong danh sách thuật toán có sẵn trên giao diện.  
- Nhấn nút **"Solve"** để thuật toán bắt đầu tìm lời giải cho trạng thái 8-Puzzle hiện tại.  
- Các bước giải được hiển thị tuần tự trên màn hình để quan sát tiến trình.  
- Có thể sử dụng nút **"Randomize"** để tạo trạng thái ban đầu ngẫu nhiên khác và thử nghiệm thuật toán.  

---

## Nhận xét tổng quát

- **Uninformed Search** thích hợp cho bài toán nhỏ, không yêu cầu heuristic, nhưng kém hiệu quả với không gian trạng thái lớn.  
- **Informed Search** tận dụng heuristic để tìm lời giải nhanh và tối ưu hơn, nhưng phụ thuộc chất lượng heuristic.  
- **Local Search** phù hợp khi không cần lời giải tối ưu, xử lý được không gian lớn nhưng có thể bị kẹt.  
- **Thuật toán môi trường phức tạp** cho bài toán có thông tin không đầy đủ hoặc đa khả năng, tuy nhiên khó triển khai và tốn tài nguyên.  
- **Thuật toán CSP** giải các bài toán có ràng buộc tốt, với các kỹ thuật tối ưu giúp giảm thời gian tìm kiếm đáng kể.


