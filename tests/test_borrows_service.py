import pytest
from uuid import uuid4

from src.api.v0.borrows.service import BorrowsService
from src.api.v0.borrows.schemas import BorrowingCreate, BorrowingReturn
from src.database.models.borrowedbook import BorrowedBook


@pytest.fixture
def mock_borrows_repo(mocker):
    return mocker.AsyncMock()


@pytest.fixture
def mock_books_repo(mocker):
    return mocker.AsyncMock()


@pytest.fixture
def service(mock_borrows_repo, mock_books_repo):
    return BorrowsService(
        borrows_repo=mock_borrows_repo, books_repo=mock_books_repo
    )


@pytest.mark.asyncio
async def test_borrow_success(service, mock_books_repo, mock_borrows_repo):
    book_uuid = uuid4()
    reader_id = 1
    responsible_id = 2

    mock_books_repo.in_stock.return_value = 2
    mock_borrows_repo.reader_borrowed_list.return_value = []
    mock_borrows_repo.borrow.return_value = BorrowedBook(uuid=uuid4())

    data = BorrowingCreate(
        book_uuid=book_uuid,
        reader_id=reader_id,
        responsible_id=responsible_id,
    )

    result = await service.borrow(data)

    assert result["message"] == "Book has been borrowed"
    assert "borrow_id" in result
    mock_books_repo.decr.assert_awaited_once_with(book_uuid)
    mock_borrows_repo.borrow.assert_awaited_once()


@pytest.mark.asyncio
async def test_borrow_no_stock(service, mock_books_repo):
    mock_books_repo.in_stock.return_value = 0
    data = BorrowingCreate(book_uuid=uuid4(), reader_id=1, responsible_id=2)

    with pytest.raises(Exception) as exc:
        await service.borrow(data)

    assert "No available copies of the book" in str(exc.value)


@pytest.mark.asyncio
async def test_borrow_limit_exceeded(
    service, mock_books_repo, mock_borrows_repo
):
    mock_books_repo.in_stock.return_value = 1
    mock_borrows_repo.reader_borrowed_list.return_value = [1, 2, 3]  # >3 books
    data = BorrowingCreate(book_uuid=uuid4(), reader_id=1, responsible_id=2)

    with pytest.raises(Exception) as exc:
        await service.borrow(data)

    assert "cannot borrow more than 3 books" in str(exc.value)


@pytest.mark.asyncio
async def test_receive_success(service, mock_borrows_repo, mock_books_repo):
    book_uuid = uuid4()
    reader_id = 1
    fake_borrow = BorrowedBook(
        uuid=uuid4(), book_uuid=book_uuid, reader_id=reader_id
    )

    mock_borrows_repo.reader_borrowed_list.return_value = [fake_borrow]

    data = BorrowingReturn(book_uuid=book_uuid, reader_id=reader_id)

    result = await service.receive(data)

    assert result["message"] == "Book successfully returned"
    mock_borrows_repo.receive.assert_awaited_once_with(fake_borrow.uuid)
    mock_books_repo.inc.assert_awaited_once_with(book_uuid)


@pytest.mark.asyncio
async def test_receive_invalid_borrow(service, mock_borrows_repo):
    data = BorrowingReturn(book_uuid=uuid4(), reader_id=1)
    mock_borrows_repo.reader_borrowed_list.return_value = []

    with pytest.raises(Exception) as exc:
        await service.receive(data)

    assert "was not borrowed by this reader" in str(exc.value)
